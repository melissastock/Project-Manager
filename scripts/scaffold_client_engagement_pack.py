#!/usr/bin/env python3

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / 'templates' / 'client-engagement-pack'

DEFAULTS = {
    'PROJECT_NAME': 'New Client Project',
    'PROJECT_FOCUS': 'product discovery and delivery planning',
    'CURRENT_PHASE': 'Discovery and planning.',
    'PRIORITY_1': 'define the immediate delivery scope',
    'PRIORITY_2': 'align documentation and ownership',
    'PRIORITY_3': 'prepare the next executable milestone',
    'ENGAGEMENT_PURPOSE': 'turn an early project concept into a clear working delivery plan',
    'STATUS_1': 'Onboarding is complete',
    'STATUS_2': 'Core ownership roles are identified',
    'STATUS_3': 'The project is ready for the next planning milestone',
    'SCOPE_1': 'clarify workflows',
    'SCOPE_2': 'define system and product boundaries',
    'SCOPE_3': 'prepare the next set of planning artifacts',
    'OUT_SCOPE_1': 'legal work unless explicitly reactivated',
    'OUT_SCOPE_2': 'production implementation unless already in an active delivery phase',
    'OUT_SCOPE_3': 'unrelated portfolio governance work',
    'PRODUCT_CONCEPT': 'A product concept description goes here.',
    'PROBLEM_STATEMENT': 'A problem statement goes here.',
    'USER_1': 'primary user',
    'USER_2': 'secondary user',
    'USER_3': 'supporting stakeholder',
    'GOAL_1': 'agree on workflow clarity',
    'GOAL_2': 'define user and role boundaries',
    'GOAL_3': 'shape the initial system context',
    'ACTOR_1': 'primary end user',
    'ACTOR_2': 'reviewer or operator',
    'ACTOR_3': 'system',
}

FILE_MAP = {
    'README.md': 'README.md',
    'engagement-overview.md': 'docs/engagement-overview.md',
    'product-brief.md': 'docs/product-brief.md',
    'working-agreement.md': 'docs/working-agreement.md',
    'discovery-plan.md': 'docs/discovery-plan.md',
    'system-context.md': 'docs/system-context.md',
}


def render(text: str, values: dict[str, str]) -> str:
    out = text
    for key, value in values.items():
        out = out.replace('{{' + key + '}}', value)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description='Scaffold the reusable client engagement doc pack into a target project.')
    parser.add_argument('--target', required=True, help='Workspace-relative or absolute path to the target repo.')
    parser.add_argument('--project-name', default=DEFAULTS['PROJECT_NAME'])
    parser.add_argument('--project-focus', default=DEFAULTS['PROJECT_FOCUS'])
    parser.add_argument('--phase', default=DEFAULTS['CURRENT_PHASE'])
    parser.add_argument('--force', action='store_true', help='Overwrite existing files.')
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target
    target.mkdir(parents=True, exist_ok=True)

    values = dict(DEFAULTS)
    values['PROJECT_NAME'] = args.project_name
    values['PROJECT_FOCUS'] = args.project_focus
    values['CURRENT_PHASE'] = args.phase

    for template_name, rel_dest in FILE_MAP.items():
        src = TEMPLATE_DIR / template_name
        dest = target / rel_dest
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and not args.force:
            continue
        dest.write_text(render(src.read_text(), values))

    print(f'Scaffolded client engagement pack into {target}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
