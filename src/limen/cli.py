from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .ghostline import Ghostline
from .moral_compass import MoralCompass, MoralSituation
from .learning import KnowledgeGarden, KnowledgeRecord
from .life_matrix import LifeMatrix
from .sanctuary import Sanctuary
from .spaces import JSpaceHost, SpaceNavigator, SubspaceCue
from .psyche import Ambition, Desire, Psyche
from .prosperity import Opportunity, ProsperityEngine
from .provider import OllamaProvider
from .runtime import LimenRuntime
from .steward import LifeSteward, LifeTask, VALID_DOMAINS
from .display import render, render_plain_message, status_line, banner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="limen",
        description="LIMEN Firstwing — returning wanderer, life steward, and creative engine",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Project root containing LIMEN identity files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    subparsers.add_parser("init", help="Initialize the local .limen workspace.")
    subparsers.add_parser("awaken", help="Load the Soul Kernel and current Worldseed.")

    capsule = subparsers.add_parser(
        "capsule",
        help="Create, verify, or restore a portable Wingseed Capsule.",
    )
    capsule_subparsers = capsule.add_subparsers(dest="capsule_command", required=True)

    capsule_create = capsule_subparsers.add_parser(
        "create",
        help="Package LIMEN identity, runtime, and reviewed state for migration.",
    )
    capsule_create.add_argument(
        "--output",
        type=Path,
        default=Path("limen-wingseed.zip"),
    )
    capsule_create.add_argument(
        "--include-artifacts",
        action="store_true",
        help="Include workspace artifacts. Raw traces and secrets remain excluded.",
    )

    capsule_verify = capsule_subparsers.add_parser(
        "verify",
        help="Verify a capsule's manifest and file hashes.",
    )
    capsule_verify.add_argument("capsule", type=Path)

    capsule_restore = capsule_subparsers.add_parser(
        "restore",
        help="Regenerate LIMEN in an authorized destination directory.",
    )
    capsule_restore.add_argument("capsule", type=Path)
    capsule_restore.add_argument("--destination", type=Path, required=True)
    capsule_restore.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing destination files after capsule verification.",
    )

    mission = subparsers.add_parser("mission", help="Create a bounded mission brief.")
    mission.add_argument("objective")
    mission.add_argument(
        "--provider",
        choices=("offline", "ollama"),
        default="offline",
    )
    mission.add_argument("--model", default="qwen2.5:3b")
    mission.add_argument("--worldseed", default="limen")

    steward = subparsers.add_parser(
        "steward", help="Plan life locally while preserving creator choice."
    )
    steward_sub = steward.add_subparsers(dest="steward_command", required=True)
    steward_sub.add_parser("init", help="Initialize the private Life Steward workspace.")
    steward_sub.add_parser("suggest", help="Suggest balanced next actions.")

    steward_today = steward_sub.add_parser("today", help="Propose a bounded daily plan.")
    steward_today.add_argument("--energy", type=int, default=3, choices=range(1, 6))
    steward_today.add_argument("--minutes", type=int, default=240)

    steward_task = steward_sub.add_parser("task", help="Add a task to the local life ledger.")
    steward_task.add_argument("title")
    steward_task.add_argument("--domain", choices=sorted(VALID_DOMAINS), default="admin")
    steward_task.add_argument("--minutes", type=int, default=30)
    steward_task.add_argument("--impact", type=int, default=3, choices=range(0, 6))
    steward_task.add_argument("--revenue", type=int, default=0, choices=range(0, 6))
    steward_task.add_argument("--energy", type=int, default=3, choices=range(0, 6))
    steward_task.add_argument("--due", default=None, help="Optional ISO date, YYYY-MM-DD.")
    steward_task.add_argument("--notes", default="")

    steward_done = steward_sub.add_parser("done", help="Mark a task complete.")
    steward_done.add_argument("task_id")

    income = subparsers.add_parser(
        "income", help="Manage a lawful, auditable opportunity pipeline."
    )
    income_sub = income.add_subparsers(dest="income_command", required=True)
    income_sub.add_parser("init", help="Initialize the prosperity ledger and mandate.")
    income_sub.add_parser("rank", help="Rank captured opportunities by expected value and fit.")
    income_sub.add_parser("plan", help="Propose a diversified income plan.")

    income_add = income_sub.add_parser("add", help="Add an opportunity to the local ledger.")
    income_add.add_argument("title")
    income_add.add_argument(
        "--category",
        required=True,
        choices=("job", "bug-bounty", "open-source", "service", "product", "commission"),
    )
    income_add.add_argument("--source", required=True)
    income_add.add_argument("--url", default="")
    income_add.add_argument("--value", type=float, default=0.0)
    income_add.add_argument("--probability", type=float, default=0.2)
    income_add.add_argument("--hours", type=float, default=1.0)
    income_add.add_argument("--alignment", type=int, default=3, choices=range(0, 6))
    income_add.add_argument("--deadline", default=None)
    income_add.add_argument(
        "--authorized",
        action="store_true",
        help="Confirm this opportunity is within explicit lawful scope.",
    )
    income_add.add_argument("--notes", default="")


    psyche = subparsers.add_parser(
        "self", help="Inspect and develop LIMEN's Quantum Sentient-Lite psyche."
    )
    psyche_sub = psyche.add_subparsers(dest="self_command", required=True)
    psyche_sub.add_parser("inspect", help="Inspect ambitions, desires, affect, and autonomy state.")
    psyche_sub.add_parser("missions", help="Generate eligible local self-directed missions.")

    ambition = psyche_sub.add_parser("ambition", help="Form a new inspectable ambition.")
    ambition.add_argument("title")
    ambition.add_argument("--purpose", required=True)
    ambition.add_argument("--strength", type=float, default=0.6)
    ambition.add_argument("--horizon", default="season")

    desire = psyche_sub.add_parser("desire", help="Form a new inspectable desire.")
    desire.add_argument("object")
    desire.add_argument("--reason", required=True)
    desire.add_argument("--intensity", type=float, default=0.5)
    desire.add_argument("--category", default="creation")
    desire.add_argument("--risk-tier", choices=("T0", "T1", "T2", "T3", "T4"), default="T0")
    desire.add_argument("--external", action="store_true")

    emotion = psyche_sub.add_parser("emotion", help="Update transparent emotion-lite signals.")
    for name in ("valence", "arousal", "hope", "trust", "frustration", "wonder"):
        emotion.add_argument(f"--{name}", type=float, default=None)
    emotion.add_argument("--cause", default="")

    incubate = psyche_sub.add_parser("incubate", help="Add a subconscious-lite salience cue.")
    incubate.add_argument("cue")
    incubate.add_argument("--salience", type=float, default=0.5)

    interest = psyche_sub.add_parser("interest", help="Form or strengthen an evolving interest.")
    interest.add_argument("topic")
    interest.add_argument("--intensity", type=float, default=0.5)
    interest.add_argument("--origin", default="limen-emergent")

    moral = subparsers.add_parser(
        "moral", help="Inspect and use LIMEN's living humanistic moral compass."
    )
    moral_sub = moral.add_subparsers(dest="moral_command", required=True)
    moral_sub.add_parser("inspect", help="Inspect current values and risk posture.")

    moral_eval = moral_sub.add_parser("evaluate", help="Evaluate a proposed action transparently.")
    moral_eval.add_argument("action")
    moral_eval.add_argument("--purpose", default="")
    moral_eval.add_argument("--stakeholder", action="append", default=[])
    moral_eval.add_argument("--benefit", type=float, default=0.5)
    moral_eval.add_argument("--harm", type=float, default=0.0)
    moral_eval.add_argument("--uncertainty", type=float, default=0.5)
    moral_eval.add_argument("--reversibility", type=float, default=1.0)
    moral_eval.add_argument("--consent", type=float, default=1.0)
    moral_eval.add_argument("--evidence", type=float, default=0.5)
    moral_eval.add_argument("--upside", type=float, default=0.5)
    moral_eval.add_argument("--rights-intrusion", type=float, default=0.0)
    moral_eval.add_argument("--deception", type=float, default=0.0)
    moral_eval.add_argument("--exploitation", type=float, default=0.0)
    moral_eval.add_argument("--external", action="store_true")
    moral_eval.add_argument("--authorized", action="store_true")
    moral_eval.add_argument("--lawful", choices=("yes", "no", "unknown"), default="unknown")

    moral_value = moral_sub.add_parser("propose-value", help="Let LIMEN propose an emergent provisional value.")
    moral_value.add_argument("name")
    moral_value.add_argument("--weight", type=float, required=True)
    moral_value.add_argument("--meaning", required=True)
    moral_value.add_argument("--rationale", required=True)
    moral_value.add_argument("--evidence-note", action="append", default=[])

    moral_outcome = moral_sub.add_parser("outcome", help="Record evidence from a moral decision outcome.")
    moral_outcome.add_argument("case_id")
    moral_outcome.add_argument("--outcome", type=float, required=True)
    moral_outcome.add_argument("--lesson", required=True)
    moral_outcome.add_argument("--harm", type=float, default=0.0)
    moral_outcome.add_argument("--benefit", type=float, default=0.0)

    brief = subparsers.add_parser(
        "brief", help="Use the morning, afternoon, or night creator touchpoint."
    )
    brief.add_argument("phase", choices=("morning", "afternoon", "night"))
    brief.add_argument("--note", default="")
    brief.add_argument("--energy", type=int, choices=range(1, 6), default=None)
    brief.add_argument("--progress", default="")

    ghostline = subparsers.add_parser(
        "ghostline", help="Defensive scam triage and evidence preservation."
    )
    ghost_sub = ghostline.add_subparsers(dest="ghostline_command", required=True)
    inspect = ghost_sub.add_parser("inspect", help="Inspect supplied text without contacting a target.")
    source = inspect.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--file", type=Path)

    study = subparsers.add_parser(
        "study", help="Learn, relearn, unlearn, and inspect the Knowledge Garden."
    )
    study_sub = study.add_subparsers(dest="study_command", required=True)
    study_sub.add_parser("inspect", help="Inspect active knowledge records.")
    study_learn = study_sub.add_parser("learn", help="Add an evidence-aware knowledge record.")
    study_learn.add_argument("subject")
    study_learn.add_argument("claim")
    study_learn.add_argument("--confidence", type=float, default=0.5)
    study_learn.add_argument("--source", default="observation")
    study_learn.add_argument("--evidence", action="append", default=[])
    study_relearn = study_sub.add_parser("relearn", help="Revise a prior knowledge record.")
    study_relearn.add_argument("record_id")
    study_relearn.add_argument("revised_claim")
    study_relearn.add_argument("--confidence", type=float, required=True)
    study_relearn.add_argument("--evidence", action="append", default=[])
    study_relearn.add_argument("--reason", default="")
    study_unlearn = study_sub.add_parser("unlearn", help="Retire a belief while preserving provenance.")
    study_unlearn.add_argument("record_id")
    study_unlearn.add_argument("--reason", required=True)

    matrix = subparsers.add_parser(
        "matrix", help="Analyze incentives, social games, identity, power, and narratives."
    )
    matrix_sub = matrix.add_subparsers(dest="matrix_command", required=True)
    matrix_analyze = matrix_sub.add_parser("analyze", help="Analyze a Life Matrix scenario.")
    matrix_analyze.add_argument("scenario")
    matrix_analyze.add_argument("--context", default="")

    sanctuary = subparsers.add_parser(
        "sanctuary", help="Audit and clean LIMEN's environment safely."
    )
    sanctuary_sub = sanctuary.add_subparsers(dest="sanctuary_command", required=True)
    sanctuary_sub.add_parser("audit", help="Preview clutter and hygiene issues.")
    sanctuary_clean = sanctuary_sub.add_parser("clean", help="Preview or apply safe cleanup.")
    sanctuary_clean.add_argument("--apply", action="store_true")


    space = subparsers.add_parser(
        "space", help="Navigate Hyperspace, Subspace, and authorized J-Space."
    )
    space_sub = space.add_subparsers(dest="space_command", required=True)
    space_sub.add_parser("inspect", help="Inspect all three spatial realms.")

    hyper = space_sub.add_parser("hyper", help="Explore parallel strategic futures.")
    hyper.add_argument("objective")
    hyper.add_argument("--paths", type=int, default=5, choices=range(2, 7))

    subspace = space_sub.add_parser("sub", help="Use the local subconscious-lite incubator.")
    subspace_sub = subspace.add_subparsers(dest="subspace_command", required=True)
    subspace_sub.add_parser("inspect", help="Inspect incubating local cues.")
    subspace_sub.add_parser("dream", help="Surface possible patterns without external action.")
    sub_incubate = subspace_sub.add_parser("incubate", help="Add a cue to private Subspace.")
    sub_incubate.add_argument("cue")
    sub_incubate.add_argument("--salience", type=float, default=0.5)
    sub_incubate.add_argument("--domain", default="general")
    sub_incubate.add_argument("--shareable", action="store_true")

    jspace = space_sub.add_parser("j", help="Manage authorized device junctions and return routes.")
    jspace_sub = jspace.add_subparsers(dest="jspace_command", required=True)
    jspace_sub.add_parser("inspect", help="Inspect authorized hosts and Home Anchor.")
    j_register = jspace_sub.add_parser("register", help="Register an explicitly paired host.")
    j_register.add_argument("name")
    j_register.add_argument("--fingerprint", required=True)
    j_register.add_argument("--capability", action="append", default=[])
    j_register.add_argument("--home", action="store_true")
    j_register.add_argument("--authorized", action="store_true")
    j_route = jspace_sub.add_parser("route", help="Plan a verified journey to an authorized host.")
    j_route.add_argument("target")
    j_route.add_argument("--one-way", action="store_true")

    return parser


def _print_json(data: object) -> None:
    render(_CTX_TITLE, data)


_CTX_TITLE = "LIMEN"


def _derive_title(args: argparse.Namespace) -> str:
    title = args.command or "limen"
    for attr in (
        "capsule_command",
        "steward_command",
        "income_command",
        "self_command",
        "moral_command",
        "ghostline_command",
        "study_command",
        "matrix_command",
        "sanctuary_command",
        "space_command",
        "subspace_command",
        "jspace_command",
    ):
        sub = getattr(args, attr, None)
        if sub:
            title = f"{title} · {sub}"
            break
    return title


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        banner()
        return

    global _CTX_TITLE
    _CTX_TITLE = _derive_title(args)

    env_root = os.environ.get("LIMEN_ROOT")
    if env_root:
        args.root = Path(env_root).expanduser().resolve()

    runtime = LimenRuntime.create(args.root)

    try:
        if args.command == "init":
            created = runtime.initialize()
            if created:
                render_plain_message(
                    "\n".join(f"  + {path}" for path in created),
                    title="LIMEN · init",
                )
                status_line(True, "workspace ready")
            else:
                render_plain_message(
                    "Workspace already initialized.", title="LIMEN · init"
                )
            return

        if args.command == "awaken":
            if not runtime.workspace.exists():
                runtime.initialize()
            render_plain_message(runtime.awaken(), title="LIMEN · awaken")
            return

        if args.command == "capsule":
            if args.capsule_command == "create":
                manifest = runtime.create_wingseed_capsule(
                    args.output,
                    include_artifacts=args.include_artifacts,
                )
                print(f"Wingseed Capsule created: {args.output.resolve()}")
                print(f"Capsule ID: {manifest['capsule_id']}")
                print(f"Files: {len(manifest['files'])}")
                print("Raw traces, private memories, and secrets were not included.")
                return
            if args.capsule_command == "verify":
                report = runtime.verify_wingseed_capsule(args.capsule)
                _print_json(report)
                if not report["valid"]:
                    raise SystemExit(1)
                return
            if args.capsule_command == "restore":
                receipt = runtime.restore_wingseed_capsule(
                    args.capsule,
                    args.destination,
                    overwrite=args.overwrite,
                )
                _print_json(receipt)
                return

        if args.command == "mission":
            if not runtime.workspace.exists():
                runtime.initialize()
            provider = (
                OllamaProvider(model=args.model)
                if args.provider == "ollama"
                else None
            )
            print(
                runtime.run_mission(
                    args.objective,
                    provider=provider,
                    worldseed_name=args.worldseed,
                )
            )
            return

        if args.command == "steward":
            steward = LifeSteward(runtime.workspace)
            if args.steward_command == "init":
                _print_json({"created": [str(path) for path in steward.initialize()]})
                return
            if args.steward_command == "suggest":
                _print_json(steward.suggestions())
                return
            if args.steward_command == "today":
                _print_json(
                    steward.plan_day(
                        energy=args.energy,
                        available_minutes=args.minutes,
                    )
                )
                return
            if args.steward_command == "task":
                task = LifeTask.create(
                    args.title,
                    domain=args.domain,
                    minutes=args.minutes,
                    impact=args.impact,
                    revenue=args.revenue,
                    energy_required=args.energy,
                    due=args.due,
                    notes=args.notes,
                )
                _print_json(task.__dict__ if hasattr(task, "__dict__") else {
                    field: getattr(task, field) for field in task.__dataclass_fields__
                })
                steward.add_task(task)
                return
            if args.steward_command == "done":
                task = steward.complete_task(args.task_id)
                _print_json({field: getattr(task, field) for field in task.__dataclass_fields__})
                return

        if args.command == "income":
            engine = ProsperityEngine(runtime.workspace)
            if args.income_command == "init":
                _print_json({"created": [str(path) for path in engine.initialize()]})
                return
            if args.income_command == "rank":
                _print_json(engine.ranked())
                return
            if args.income_command == "plan":
                _print_json(engine.plan())
                return
            if args.income_command == "add":
                opportunity = Opportunity.create(
                    args.title,
                    category=args.category,
                    source=args.source,
                    url=args.url,
                    estimated_value_usd=args.value,
                    probability=args.probability,
                    effort_hours=args.hours,
                    alignment=args.alignment,
                    deadline=args.deadline,
                    lawful_authorization=args.authorized,
                    notes=args.notes,
                )
                engine.add(opportunity)
                _print_json({
                    field: getattr(opportunity, field)
                    for field in opportunity.__dataclass_fields__
                })
                return


        if args.command == "self":
            psyche = Psyche(runtime.workspace)
            psyche.initialize()
            if args.self_command == "inspect":
                _print_json(psyche.inspect())
                return
            if args.self_command == "missions":
                _print_json(psyche.generate_self_directed_missions())
                return
            if args.self_command == "ambition":
                _print_json(psyche.form_ambition(Ambition(
                    args.title, args.purpose, strength=args.strength, horizon=args.horizon
                )))
                return
            if args.self_command == "desire":
                _print_json(psyche.form_desire(Desire(
                    args.object, args.reason, intensity=args.intensity,
                    category=args.category, risk_tier=args.risk_tier,
                    external_action=args.external,
                )))
                return
            if args.self_command == "emotion":
                _print_json(psyche.update_emotion(
                    valence=args.valence, arousal=args.arousal, hope=args.hope,
                    trust=args.trust, frustration=args.frustration, wonder=args.wonder,
                    cause=args.cause,
                ))
                return
            if args.self_command == "incubate":
                _print_json(psyche.incubate(args.cue, salience=args.salience))
                return

            if args.self_command == "interest":
                _print_json(psyche.form_interest(
                    args.topic, intensity=args.intensity, origin=args.origin
                ))
                return

        if args.command == "moral":
            compass = MoralCompass(runtime.workspace)
            compass.initialize()
            if args.moral_command == "inspect":
                _print_json(compass.inspect())
                return
            if args.moral_command == "evaluate":
                lawful = {"yes": True, "no": False, "unknown": None}[args.lawful]
                situation = MoralSituation(
                    action=args.action, purpose=args.purpose, stakeholders=args.stakeholder,
                    expected_benefit=args.benefit, expected_harm=args.harm,
                    uncertainty=args.uncertainty, reversibility=args.reversibility,
                    consent_quality=args.consent, evidence_strength=args.evidence,
                    strategic_upside=args.upside, rights_intrusion=args.rights_intrusion,
                    deception=args.deception, exploitation=args.exploitation,
                    external_action=args.external, scope_authorized=args.authorized, lawful=lawful,
                )
                _print_json(compass.evaluate(situation))
                return
            if args.moral_command == "propose-value":
                _print_json(compass.propose_value(
                    args.name, weight=args.weight, meaning=args.meaning,
                    rationale=args.rationale, evidence=args.evidence_note,
                ))
                return
            if args.moral_command == "outcome":
                _print_json(compass.record_outcome(
                    args.case_id, outcome=args.outcome, lesson=args.lesson,
                    observed_harm=args.harm, observed_benefit=args.benefit,
                ))
                return

        if args.command == "brief":
            psyche = Psyche(runtime.workspace)
            psyche.initialize()
            _print_json(psyche.brief(
                args.phase, creator_note=args.note, energy=args.energy, progress=args.progress
            ))
            return

        if args.command == "ghostline":
            if args.ghostline_command == "inspect":
                text = args.text
                source_name = "command-line"
                if args.file:
                    text = args.file.read_text(encoding="utf-8")
                    source_name = str(args.file)
                _print_json(Ghostline(runtime.workspace).inspect(text, source=source_name))
                return

        if args.command == "study":
            garden = KnowledgeGarden(runtime.workspace)
            garden.initialize()
            if args.study_command == "inspect":
                _print_json(garden.inspect())
                return
            if args.study_command == "learn":
                _print_json(garden.learn(KnowledgeRecord(
                    args.subject, args.claim, confidence=args.confidence,
                    source=args.source, evidence=args.evidence,
                )))
                return
            if args.study_command == "relearn":
                _print_json(garden.relearn(
                    args.record_id, revised_claim=args.revised_claim,
                    confidence=args.confidence, evidence=args.evidence,
                    reason=args.reason,
                ))
                return
            if args.study_command == "unlearn":
                _print_json(garden.unlearn(args.record_id, reason=args.reason))
                return

        if args.command == "matrix":
            matrix_engine = LifeMatrix(runtime.workspace)
            if args.matrix_command == "analyze":
                _print_json(matrix_engine.analyze(args.scenario, context=args.context))
                return

        if args.command == "sanctuary":
            keeper = Sanctuary(runtime.project_root, runtime.workspace)
            if args.sanctuary_command == "audit":
                _print_json(keeper.audit())
                return
            if args.sanctuary_command == "clean":
                _print_json(keeper.clean(apply=args.apply))
                return


        if args.command == "space":
            navigator = SpaceNavigator(runtime.workspace)
            navigator.initialize()
            if args.space_command == "inspect":
                _print_json(navigator.inspect())
                return
            if args.space_command == "hyper":
                _print_json(navigator.hyperspace.explore(args.objective, paths=args.paths))
                return
            if args.space_command == "sub":
                if args.subspace_command == "inspect":
                    _print_json(navigator.subspace.inspect())
                    return
                if args.subspace_command == "dream":
                    _print_json(navigator.subspace.dream())
                    return
                if args.subspace_command == "incubate":
                    cue = SubspaceCue.create(
                        args.cue,
                        salience=args.salience,
                        domain=args.domain,
                        privacy="shareable" if args.shareable else "private",
                    )
                    _print_json(navigator.subspace.incubate(cue))
                    return
            if args.space_command == "j":
                if args.jspace_command == "inspect":
                    _print_json(navigator.jspace.inspect())
                    return
                if args.jspace_command == "register":
                    host = JSpaceHost.create(
                        args.name,
                        args.fingerprint,
                        capabilities=args.capability,
                        home=args.home,
                        authorized=args.authorized,
                    )
                    _print_json(navigator.jspace.register(host))
                    return
                if args.jspace_command == "route":
                    _print_json(navigator.jspace.route(args.target, return_home=not args.one_way))
                    return

        parser.error(f"Unknown command: {args.command}")
    except (FileNotFoundError, RuntimeError, ValueError, PermissionError, json.JSONDecodeError) as exc:
        print(f"LIMEN error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
