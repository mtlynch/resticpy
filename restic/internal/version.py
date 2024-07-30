import json
import re

from restic.internal import command_executor


def run(restic_base_command):
    cmd = restic_base_command + ['version']
    out = command_executor.execute(cmd)
    try:
        return _parse_json(out)
    except json.decoder.JSONDecodeError:
        # Restic prior to 0.17.0 ignored the JSON flag and returned version info
        # in plaintext, so try to parse the plaintext.
        return _parse_plaintext(out)


def _parse_json(version_result):
    parsed = json.loads(version_result)
    return {
        'restic_version': parsed['version'],
        'go_version': parsed['go_version'].replace('go', ''),
        'platform_version': parsed['go_os'],
        'architecture': parsed['go_arch']
    }


def _parse_plaintext(version_result):
    match = re.match((r'restic ([0-9\.]+) compiled with go([0-9\.]+) '
                      'on ([a-zA-Z0-9]+)/([a-zA-Z0-9]+)'), version_result)
    return {
        'restic_version': match.group(1),
        'go_version': match.group(2),
        'platform_version': match.group(3),
        'architecture': match.group(4)
    }
