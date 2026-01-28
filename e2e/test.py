#!/usr/bin/env python3

import json
import logging
import os.path
import tempfile

import restic

logger = logging.getLogger(__name__)

# pylint: disable=consider-using-with


def configure_logging():

    class ShutdownHandler(logging.StreamHandler):

        def emit(self, record):
            super().emit(record)
            if record.levelno >= logging.CRITICAL:
                raise SystemExit(255)

    root_logger = logging.getLogger()
    handler = ShutdownHandler()
    formatter = logging.Formatter("%(name)-15s %(levelname)-4s %(message)s")
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)


def print_version():
    version_info = restic.version()
    logger.info(
        "Running end-to-end tests with restic version %s (%s/%s/go%s)",
        version_info["restic_version"],
        version_info["architecture"],
        version_info["platform_version"],
        version_info["go_version"],
    )


def test_basic_backup_and_restore():
    password = "mysecretpass"
    password_file = tempfile.NamedTemporaryFile(mode="w+t", encoding="utf-8")
    password_file.write(password)
    password_file.flush()

    dummy_source_dir = tempfile.mkdtemp()
    dummy_data_path = os.path.join(dummy_source_dir, "mydata.txt")
    with open(dummy_data_path, "w", encoding="utf-8") as dummy_data_file:
        dummy_data_file.write("some data to back up")

    primary_repo = tempfile.mkdtemp()

    restic.repository = primary_repo
    restic.password_file = password_file.name

    logger.info("Initializing repository")
    logger.info(restic.init())

    logger.info("Backing up %s", dummy_data_path)
    backup_result = restic.backup(paths=[dummy_data_path])
    logger.info("backup_result: %s", json.dumps(backup_result))
    if backup_result["files_new"] != 1:
        logger.error("Expected 1 new file (got %d)", backup_result["files_new"])
        return False
    if backup_result["files_changed"] != 0:
        logger.error(
            "Expected 0 changed files (got %d)", backup_result["files_changed"]
        )
        return False

    logger.info("Finding files")
    find1_result = restic.find("mydata.txt")
    if (
        len(find1_result) != 1
        or "matches" not in find1_result[0]
        or len(find1_result[0]["matches"]) != 1
    ):
        logger.error(
            "Expected to find exactly 1 match, instead got result %s", find1_result
        )
        return False
    find2_result = restic.find("non-existent-file.txt")
    if len(find2_result) > 0:
        logger.error(
            "Expected to not find any matches, instead got result %s", find2_result
        )
        return False

    restore_dir = tempfile.mkdtemp()
    logger.info("Restoring to %s", restore_dir)
    logger.info(restic.restore(snapshot_id="latest", target_dir=restore_dir))

    restored_data_path = os.path.join(restore_dir, dummy_data_path)
    if not os.path.exists(restored_data_path):
        logger.error("Expected to find %s", restored_data_path)
        return False
    restored_data_expected = "some data to back up"
    with open(restored_data_path, encoding="utf-8") as restored_file:
        restored_data_actual = restored_file.read()
    if restored_data_expected != restored_data_actual:
        logger.error(
            "Expected to restored file to contain %s (got %s)",
            restored_data_expected,
            restored_data_actual,
        )
        return False

    snapshots = restic.snapshots(group_by=["host"])
    logger.info("repo snapshots: %s", json.dumps(snapshots))
    if len(snapshots) != 1:
        logger.error("Expected snapshots to return a single object")
        return False
    if len(snapshots[0]["snapshots"]) != 1:
        logger.error("Expected snapshots key to contain a single object")
        return False

    logger.info("Overwriting contents of %s with new data", dummy_data_path)
    with open(dummy_data_path, "w", encoding="utf-8") as dummy_data_file:
        dummy_data_file.write("a new version of the file")

    logger.info("Backing up %s (after edit)", dummy_data_path)
    backup_result = restic.backup(paths=[dummy_data_path])
    logger.info("backup_result: %s", json.dumps(backup_result))
    if backup_result["files_new"] != 0:
        logger.error("Expected 0 new file (got %d)", backup_result["files_new"])
        return False
    if backup_result["files_changed"] != 1:
        logger.error("Expected 1 changed file (got %d)", backup_result["files_changed"])
        return False

    snapshots = restic.snapshots(group_by=["host"])
    logger.info("repo snapshots: %s", json.dumps(snapshots))
    if len(snapshots) != 1:
        logger.error("Expected snapshots to return a single object")
        return False
    if len(snapshots[0]["snapshots"]) != 2:
        logger.error("Expected snapshots key to contain two snapshots")
        return False

    stats = restic.stats(mode="blobs-per-file")
    logger.info("repo stats: %s", stats)
    expected_size = len(restored_data_expected) + len("a new version of the file")
    if stats["total_size"] != expected_size:
        logger.error(
            "Expected total size of %d (got %d)", expected_size, stats["total_size"]
        )
        return False

    logger.info("check result: %s", restic.check(read_data=True))
    return True


def test_rewrite_snapshot():
    password = "mysecretpass"
    password_file = tempfile.NamedTemporaryFile(mode="w+t", encoding="utf-8")
    password_file.write(password)
    password_file.flush()

    dummy_source_dir = tempfile.mkdtemp()
    dummy_path1 = os.path.join(dummy_source_dir, "data1.txt")
    with open(dummy_path1, "w", encoding="utf-8") as dummy_data_file:
        dummy_data_file.write("some data to back up")
    dummy_path2 = os.path.join(dummy_source_dir, "data2.txt")
    with open(dummy_path2, "w", encoding="utf-8") as dummy_data_file:
        dummy_data_file.write("another file I have")

    primary_repo = tempfile.mkdtemp()

    restic.repository = primary_repo
    restic.password_file = password_file.name

    logger.info("Initializing repository")
    logger.info(restic.init())

    paths = [dummy_path1, dummy_path2]
    logger.info("Backing up %s", paths)
    backup_result = restic.backup(paths=paths)
    logger.info("backup_result: %s", json.dumps(backup_result))
    if backup_result["files_new"] != 2:
        logger.error("Expected 2 new file (got %d)", backup_result["files_new"])
        return False
    if backup_result["files_changed"] != 0:
        logger.error(
            "Expected 0 changed files (got %d)", backup_result["files_changed"]
        )
        return False

    snapshots = restic.snapshots()
    logger.info("repo snapshots (before rewrite): %s", json.dumps(snapshots))
    original_snapshot_id = snapshots[0]["id"]

    restic.rewrite(exclude=[dummy_path2], forget=True)

    snapshots = restic.snapshots()
    logger.info("repo snapshots (after rewrite): %s", json.dumps(snapshots))
    if snapshots[0]["id"] == original_snapshot_id:
        logger.error(
            "expected snapshot ID %s to change after rewrite", original_snapshot_id
        )
        return False
    if snapshots[0]["original"] != original_snapshot_id:
        logger.error(
            "expected snapshot to refer to original snapshot ID (%s), got %s",
            original_snapshot_id,
            snapshots[0]["original"],
        )
        return False

    logger.info("Verifying preserved file still exists in repo")
    find1_result = restic.find("data1.txt")
    if (
        len(find1_result) != 1
        or "matches" not in find1_result[0]
        or len(find1_result[0]["matches"]) != 1
    ):
        logger.error(
            "Expected to find exactly 1 match, instead got result %s", find1_result
        )
        return False

    logger.info("Verifying excluded file no longer exists in repo")
    find2_result = restic.find("data2.txt")
    if len(find2_result) > 0:
        logger.error(
            ("Expected to not find file deleted in rewrite, instead got result " "%s"),
            find2_result,
        )
        return False

    return True


def test_change_keys():
    password = "mysecretpass"
    password_file = tempfile.NamedTemporaryFile(mode="w+t", encoding="utf-8")
    password_file.write(password)
    password_file.flush()

    dummy_source_dir = tempfile.mkdtemp()
    dummy_data_path = os.path.join(dummy_source_dir, "mydata.txt")
    with open(dummy_data_path, "w", encoding="utf-8") as dummy_data_file:
        dummy_data_file.write("some data to back up")

    primary_repo = tempfile.mkdtemp()

    restic.repository = primary_repo
    restic.password_file = password_file.name

    logger.info("Initializing repository")
    logger.info(restic.init())

    logger.info("Backing up %s", dummy_data_path)
    backup_result = restic.backup(paths=[dummy_data_path])
    logger.info("backup_result: %s", json.dumps(backup_result))
    if backup_result["files_new"] != 1:
        logger.error("Expected 1 new file (got %d)", backup_result["files_new"])
        return False
    if backup_result["files_changed"] != 0:
        logger.error(
            "Expected 0 changed files (got %d)", backup_result["files_changed"]
        )
        return False

    repo_keys = restic.key.list()
    logger.info("repo keys: %s", repo_keys)
    repo_keys_len_expected = 1
    repo_keys_len_actual = len(repo_keys)
    if repo_keys_len_expected != repo_keys_len_actual:
        logger.error(
            "Expected key count of %d (got %d)",
            repo_keys_len_expected,
            repo_keys_len_actual,
        )
        return False

    password2 = "mysecretpass2"
    password2_file = tempfile.NamedTemporaryFile(mode="w+t", encoding="utf-8")
    password2_file.write(password2)
    password2_file.flush()
    logger.info(
        "adding a repo key: %s", restic.key.add(new_password_file=password2_file.name)
    )

    repo_keys = restic.key.list()
    logger.info("after changing key, repo keys: %s", repo_keys)
    repo_keys_len_expected = 2
    repo_keys_len_actual = len(repo_keys)
    if repo_keys_len_expected != repo_keys_len_actual:
        logger.error(
            "Expected key count of %d (got %d)",
            repo_keys_len_expected,
            repo_keys_len_actual,
        )
        return False

    restic.password_file = password2_file.name
    with tempfile.NamedTemporaryFile(mode="wt", encoding="utf-8") as password3_file:
        password3 = "mysecretpass3"
        password3_file.write(password3)
        password3_file.flush()
        logger.info(
            "changing repo default key: %s",
            restic.key.passwd(new_password_file=password3_file.name),
        )

    restic.password_file = password_file.name
    repo_keys = restic.key.list()
    logger.info("after changing key, repo keys: %s", repo_keys)

    unused_key = [key for key in restic.key.list() if not key["current"]][0]
    logger.info("removing unused repo key: %s", restic.key.remove(unused_key["id"]))
    repo_keys = restic.key.list()
    repo_keys_len_expected = 1
    repo_keys_len_actual = len(repo_keys)
    if repo_keys_len_expected != repo_keys_len_actual:
        logger.error(
            "Expected key count of %d (got %d)",
            repo_keys_len_expected,
            repo_keys_len_actual,
        )
        return False

    return True


def test_print_config_and_objects():
    password = "mysecretpass"
    password_file = tempfile.NamedTemporaryFile(mode="w+t", encoding="utf-8")
    password_file.write(password)
    password_file.flush()

    dummy_source_dir = tempfile.mkdtemp()
    dummy_data_path = os.path.join(dummy_source_dir, "mydata.txt")
    with open(dummy_data_path, "w", encoding="utf-8") as dummy_data_file:
        dummy_data_file.write("some data to back up")

    primary_repo = tempfile.mkdtemp()

    restic.repository = primary_repo
    restic.password_file = password_file.name

    logger.info("Initializing repository")
    logger.info(restic.init())

    logger.info("Backing up %s", dummy_data_path)
    backup_result = restic.backup(paths=[dummy_data_path])
    logger.info("backup_result: %s", json.dumps(backup_result))
    if backup_result["files_new"] != 1:
        logger.error("Expected 1 new file (got %d)", backup_result["files_new"])
        return False
    if backup_result["files_changed"] != 0:
        logger.error(
            "Expected 0 changed files (got %d)", backup_result["files_changed"]
        )
        return False

    logger.info("repository config: %s", restic.cat.config())
    logger.info("repository masterkey: %s", restic.cat.masterkey())

    logger.info("repository locks: %s", restic.list.locks())

    return True


def test_prune():
    password = "mysecretpass"
    password_file = tempfile.NamedTemporaryFile(mode="w+t", encoding="utf-8")
    password_file.write(password)
    password_file.flush()

    dummy_source_dir = tempfile.mkdtemp()
    dummy_data_path = os.path.join(dummy_source_dir, "mydata.txt")
    with open(dummy_data_path, "w", encoding="utf-8") as dummy_data_file:
        dummy_data_file.write("some data to back up")

    primary_repo = tempfile.mkdtemp()

    restic.repository = primary_repo
    restic.password_file = password_file.name

    logger.info("Initializing repository")
    logger.info(restic.init())

    logger.info("Backing up %s", dummy_data_path)
    backup_result = restic.backup(paths=[dummy_data_path])
    logger.info("backup_result: %s", json.dumps(backup_result))
    if backup_result["files_new"] != 1:
        logger.error("Expected 1 new file (got %d)", backup_result["files_new"])
        return False
    if backup_result["files_changed"] != 0:
        logger.error(
            "Expected 0 changed files (got %d)", backup_result["files_changed"]
        )
        return False

    logger.info("pruning repo: %s", restic.forget(prune=True, keep_daily=5))

    return True


def test_copy_repo():
    password = "mysecretpass"
    password_file = tempfile.NamedTemporaryFile(mode="w+t", encoding="utf-8")
    password_file.write(password)
    password_file.flush()

    dummy_source_dir = tempfile.mkdtemp()
    dummy_data_path = os.path.join(dummy_source_dir, "mydata.txt")
    with open(dummy_data_path, "w", encoding="utf-8") as dummy_data_file:
        dummy_data_file.write("some data to back up")

    primary_repo = tempfile.mkdtemp()

    restic.repository = primary_repo
    restic.password_file = password_file.name

    logger.info("Initializing repository")
    logger.info(restic.init())

    logger.info("Backing up %s", dummy_data_path)
    backup_result = restic.backup(paths=[dummy_data_path])
    logger.info("backup_result: %s", json.dumps(backup_result))
    if backup_result["files_new"] != 1:
        logger.error("Expected 1 new file (got %d)", backup_result["files_new"])
        return False
    if backup_result["files_changed"] != 0:
        logger.error(
            "Expected 0 changed files (got %d)", backup_result["files_changed"]
        )
        return False

    # Initialiize a secondary repo
    logger.info("making secondary repository")

    password4 = "mysecretpass4"
    password4_file = tempfile.NamedTemporaryFile(mode="wt", encoding="utf-8")
    password4_file.write(password4)
    password4_file.flush()

    secondary_repo = tempfile.mkdtemp()

    restic.repository = secondary_repo
    restic.password_file = password4_file.name

    logger.info(restic.init())
    logger.info(
        "repo copy result: %s",
        restic.copy(from_repo=primary_repo, from_password_file=password_file.name),
    )

    return True


def main():
    configure_logging()

    restic.binary_path = "restic"
    print_version()

    tests = [
        test_basic_backup_and_restore,
        test_rewrite_snapshot,
        test_change_keys,
        test_print_config_and_objects,
        test_prune,
        test_copy_repo,
    ]
    successes = 0
    for testcase in tests:
        logger.info("*" * 80)
        logger.info("Starting end-to-end test: %s", testcase.__name__)
        logger.info("*" * 80)
        try:
            if testcase():
                successes += 1
        # pylint: disable=broad-except
        except Exception as e:
            logger.error("%s failed: %s", testcase.__name__, e)
    failures = len(tests) - successes
    logger.info("%d/%d end-to-end tests succeeded", successes, len(tests))
    if failures:
        logger.fatal("%d end-to-end tests failed", failures)


if __name__ == "__main__":
    main()
