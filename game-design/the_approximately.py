"""
the_approximately.py — A simulation of The Approximately game.

Demonstrates:
    - Position generation from prompts
    - Gap-finding between positions (resonance scoring)
    - Fibonacci Tunnel surfacing
    - Anti-monoculture enforcement

Run: python3 the_approximately.py
"""

import random
import math
import textwrap
from dataclasses import dataclass, field
from typing import Optional
import numpy as np

# ---------------------------------------------------------------------------
# Game Content
# ---------------------------------------------------------------------------

PROMPTS = [
    "What is consciousness?",
    "Design a door for someone who fears enclosed spaces.",
    "Translate 'nostalgia' into architecture.",
    "What does the number 7 smell like?",
    "Describe the sound of an idea arriving.",
    "What shape is a conversation between two strangers?",
    "Build a machine that measures longing.",
    "What is the half-life of a secret?",
    "Design a clock for someone who experiences time non-linearly.",
    "What color is the space between two thoughts?",
]

PERSPECTIVES = [
    "As a mathematician",
    "As a child seeing snow for the first time",
    "As someone who has lived 10,000 years",
    "As a machine learning to dream",
    "As a cartographer of emotions",
    "As a chef who cooks with sound",
    "As an archaeologist of the future",
    "As a translator who only speaks in metaphors",
    "As a gardener growing memories",
    "As an architect who designs silence",
]

# Simple word embeddings (mock: each word → a deterministic random vector)
EMBED_DIM = 32
_word_cache: dict[str, np.ndarray] = {}


def embed(text: str) -> np.ndarray:
    """Embed text using word hashing into a fixed-dimensional vector."""
    vec = np.zeros(EMBED_DIM)
    words = text.lower().split()
    for w in words:
        if w not in _word_cache:
            rng = np.random.default_rng(hash(w) % (2**32))
            _word_cache[w] = rng.normal(size=EMBED_DIM)
        vec += _word_cache[w]
    return vec / (np.linalg.norm(vec) + 1e-9)


# ---------------------------------------------------------------------------
# Game State
# ---------------------------------------------------------------------------

@dataclass
class Position:
    player: str
    prompt: str
    perspective: str
    text: str
    vector: np.ndarray


@dataclass
class GapFinding:
    finder: str
    pos_a: str  # player name
    pos_b: str  # player name
    description: str
    resonance_score: float
    novelty_score: float


@dataclass
class GameState:
    round_number: int = 0
    positions: list[Position] = field(default_factory=list)
    history: list[list[Position]] = field(default_factory=list)
    gaps: list[GapFinding] = field(default_factory=list)
    scores: dict[str, int] = field(default_factory=dict)
    tunnel_events: list[dict] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Position Generation
# ---------------------------------------------------------------------------

POSITION_TEMPLATES = [
    "{prompt_answer} — {perspective_flavor}",
    "It is {metaphor}. {perspective_flavor}.",
    "The answer is not {negation} but {affirmation}.",
    "Imagine: {image}. That is the answer.",
]


def generate_position(player: str, prompt: str, perspective: str) -> str:
    """Generate a position for a player given a prompt and perspective."""
    # This is a simulation — in the real game, players write these.
    # Here we generate them from templates to demonstrate the mechanics.

    rng = random.Random(hash(player + prompt + perspective) % (2**32))

    answers = {
        "What is consciousness?": ["a mirror looking at itself", "the story the brain tells itself",
                                    "the echo of attention", "what happens when matter dreams"],
        "Design a door for someone who fears enclosed spaces.": ["a door that is already open",
                                                                  "a threshold made of light",
                                                                  "a door that opens both ways at once"],
        "Translate 'nostalgia' into architecture.": ["rooms that are slightly too small",
                                                       "stairs that lead to childhood",
                                                       "windows facing the past"],
        "What does the number 7 smell like?": ["cinnamon and old paper",
                                                "the air before a thunderstorm",
                                                "woodsmoke and mathematics"],
        "Describe the sound of an idea arriving.": ["a key turning in a lock you forgot existed",
                                                      "the intake of breath before speaking",
                                                      "silence getting louder"],
        "What shape is a conversation between two strangers?": ["a spiral slowly finding its center",
                                                                  "two rivers briefly merging",
                                                                  "a chess game with no board"],
        "Build a machine that measures longing.": ["a compass that points to what you've lost",
                                                     "a clock that ticks backwards to the last time",
                                                     "a scale that weighs absence"],
        "What is the half-life of a secret?": ["it depends on how many people love you",
                                                 "exactly one conversation after midnight",
                                                 "longer than guilt, shorter than shame"],
        "Design a clock for someone who experiences time non-linearly.": ["a clock with no face, only hands that move when they need to",
                                                                            "a clock made of memories arranged by feeling",
                                                                            "a spiral that opens and closes"],
        "What color is the space between two thoughts?": ["the blue of almost-remembering",
                                                            "the clear of a held breath",
                                                            "the grey of potential"],
    }

    flavors = {
        "As a mathematician": "The equation is elegant but unsolvable",
        "As a child seeing snow for the first time": "Everything is new and slightly cold",
        "As someone who has lived 10,000 years": "I have seen this before, but never like this",
        "As a machine learning to dream": "I process this in gradients, not certainties",
        "As a cartographer of emotions": "Here be dragons, here be comfort",
        "As a chef who cooks with sound": "The ingredients are frequency and silence",
        "As an archaeologist of the future": "I excavate what hasn't happened yet",
        "As a translator who only speaks in metaphors": "I render this as image, not argument",
        "As a gardener growing memories": "This blooms in the shade of attention",
        "As an architect who designs silence": "I build the space around the answer",
    }

    answer = rng.choice(answers.get(prompt, ["something undefined"]))
    flavor = flavors.get(perspective, "from a unique vantage")
    negation = rng.choice(answer.split())
    affirmation = rng.choice([w for w in answer.split() if w != negation] or answer.split())

    template = rng.choice(POSITION_TEMPLATES)
    text = template.format(
        prompt_answer=answer,
        perspective_flavor=flavor,
        metaphor=answer,
        negation=negation,
        affirmation=affirmation,
        image=answer,
    )

    return text


def take_position(player: str, prompt: str, perspective: str) -> Position:
    """A player takes a position on a prompt."""
    text = generate_position(player, prompt, perspective)
    vec = embed(text)
    return Position(
        player=player,
        prompt=prompt,
        perspective=perspective,
        text=text,
        vector=vec,
    )


# ---------------------------------------------------------------------------
# Gap Finding
# ---------------------------------------------------------------------------

def find_gap(
    finder: str,
    pos_a: Position,
    pos_b: Position,
    finder_vector: Optional[np.ndarray] = None,
) -> GapFinding:
    """Find the gap between two positions.

    The gap is the territory between two positions — what they imply
    but neither states.
    """
    # Compute the midpoint vector (the "between")
    midpoint = (pos_a.vector + pos_b.vector) / 2
    mid_norm = midpoint / (np.linalg.norm(midpoint) + 1e-9)

    # Resonance: how aligned are the two position VECTORS' relationship
    # to the finder's vector? High resonance means the finder found
    # something that both positions point toward.
    if finder_vector is not None:
        f_norm = finder_vector / (np.linalg.norm(finder_vector) + 1e-9)
        resonance = float(np.dot(mid_norm, f_norm))
    else:
        # Without a finder vector, estimate resonance from position alignment
        a_norm = pos_a.vector / (np.linalg.norm(pos_a.vector) + 1e-9)
        b_norm = pos_b.vector / (np.linalg.norm(pos_b.vector) + 1e-9)
        position_sim = float(np.dot(a_norm, b_norm))
        # High similarity → low gap-finding potential → lower resonance
        resonance = max(0.0, 1.0 - abs(position_sim))

    # Novelty: distance from midpoint to the centroid of ALL positions
    # (how far is this gap from the obvious center?)
    novelty = float(np.linalg.norm(midpoint))

    # Generate gap description
    gap_desc = describe_gap(pos_a, pos_b)

    # Scale scores
    res_score = round(resonance * 5, 1)
    res_score = max(0, min(5, res_score))
    nov_score = round(min(novelty * 3, 3), 1)
    nov_score = max(0, min(3, nov_score))

    return GapFinding(
        finder=finder,
        pos_a=pos_a.player,
        pos_b=pos_b.player,
        description=gap_desc,
        resonance_score=res_score,
        novelty_score=nov_score,
    )


def describe_gap(pos_a: Position, pos_b: Position) -> str:
    """Describe the gap between two positions."""
    a_words = set(pos_a.text.lower().split())
    b_words = set(pos_b.text.lower().split())
    shared = a_words & b_words - {"the", "a", "is", "to", "and", "of", "it", "that", "but", "not"}

    if shared:
        return f"The space where {' '.join(shared)} becomes a question neither of you asked."
    else:
        return f"The territory between '{pos_a.text[:30]}...' and '{pos_b.text[:30]}...' that both imply and neither claims."


# ---------------------------------------------------------------------------
# Anti-Monoculture Check
# ---------------------------------------------------------------------------

def check_monoculture(positions: list[Position], threshold: float = 0.85) -> list[tuple[str, str]]:
    """Check if any two positions are too similar."""
    violations = []
    for i, a in enumerate(positions):
        for b in positions[i + 1:]:
            sim = float(np.dot(a.vector, b_vector(b)))
            if sim > threshold:
                violations.append((a.player, b.player))
    return violations


def b_vector(pos: Position) -> np.ndarray:
    """Normalized position vector."""
    return pos.vector / (np.linalg.norm(pos.vector) + 1e-9)


# ---------------------------------------------------------------------------
# Fibonacci Tunnel
# ---------------------------------------------------------------------------

def fibonacci_tunnel(
    all_positions: list[Position],
    current_positions: list[Position],
    round_number: int,
    n: int = 8,
) -> Optional[Position]:
    """Surface the position most distant from the current chord.

    Every n rounds, find the old position with the lowest resonance
    to the current cluster of positions.
    """
    if round_number % n != 0 or round_number == 0:
        return None

    if len(all_positions) < n:
        return None

    # Current chord = centroid of current positions
    current_centroid = np.mean([p.vector for p in current_positions], axis=0)
    current_norm = current_centroid / (np.linalg.norm(current_centroid) + 1e-9)

    # Find most distant past position
    most_distant = None
    max_distance = -1

    for pos in all_positions:
        if pos in current_positions:
            continue
        pos_norm = pos.vector / (np.linalg.norm(pos.vector) + 1e-9)
        resonance = float(np.dot(pos_norm, current_norm))
        distance = 1.0 - resonance
        if distance > max_distance:
            max_distance = distance
            most_distant = pos

    return most_distant


# ---------------------------------------------------------------------------
# Game Simulation
# ---------------------------------------------------------------------------

def simulate_round(state: GameState, players: list[str], prompt: str) -> None:
    """Simulate one round of The Approximately."""
    state.round_number += 1
    round_num = state.round_number

    print(f"\n{'='*60}")
    print(f"  ROUND {round_num}")
    print(f"  Prompt: \"{prompt}\"")
    print(f"{'='*60}")

    # Phase 1: Each player takes a position
    state.positions = []
    perspectives = random.sample(PERSPECTIVES, len(players))

    print("\n--- POSITIONS ---")
    for player, perspective in zip(players, perspectives):
        pos = take_position(player, prompt, perspective)
        state.positions.append(pos)
        print(f"\n  {player} ({perspective}):")
        print(f"    \"{pos.text}\"")

    # Phase 2: Check for monoculture
    violations = check_monoculture(state.positions)
    if violations:
        print("\n--- ANTI-MONOCULTURE WARNING ---")
        for a, b in violations:
            print(f"  ⚠ {a} and {b} are too similar. One must change direction next round.")

    # Phase 3: Each player finds a gap
    print("\n--- THE GAP ---")
    for finder in players:
        others = [p for p in state.positions if p.player != finder]
        if len(others) < 2:
            continue

        # Pick the two most different positions for the richest gap
        best_pair = (others[0], others[1])
        best_dist = 0
        for i, a in enumerate(others):
            for b in others[i + 1:]:
                d = np.linalg.norm(a.vector - b.vector)
                if d > best_dist:
                    best_dist = d
                    best_pair = (a, b)

        gap = find_gap(finder, best_pair[0], best_pair[1])
        state.gaps.append(gap)

        total = gap.resonance_score + gap.novelty_score

        # Fibonacci bonus
        fib_bonus = 0
        if round_num % 8 == 0:
            fib_bonus = 5
            print(f"\n  🔮 FIBONACCI TUNNEL ACTIVE (Round {round_num})")

        print(f"\n  {finder} finds the gap between {gap.pos_a} and {gap.b}:")
        print(f"    \"{gap.description}\"")
        print(f"    Resonance: {gap.resonance_score}/5 | Novelty: {gap.novelty_score}/3 | Fibonacci: +{fib_bonus}")
        print(f"    TOTAL: {total + fib_bonus:.1f}")

        state.scores[finder] = state.scores.get(finder, 0) + int(total + fib_bonus)

    # Phase 4: Fibonacci Tunnel surfacing
    all_historical = [p for round_positions in state.history for p in round_positions]
    all_historical += state.positions

    tunneled = fibonacci_tunnel(all_historical, state.positions, round_num)
    if tunneled:
        print(f"\n--- TUNNEL SURFACED ---")
        print(f"  From Round ? | {tunneled.player}: \"{tunneled.text[:60]}...\"")
        print(f"  This forgotten position resonates with the present.")
        state.tunnel_events.append({
            "round": round_num,
            "player": tunneled.player,
            "text": tunneled.text,
        })

    # Save positions to history
    state.history.append(state.positions.copy())

    # Score display
    print(f"\n--- SCORES ---")
    for player in sorted(state.scores, key=lambda p: -state.scores[p]):
        print(f"  {player}: {state.scores[player]} points")


def simulate_game():
    """Run a full simulation of The Approximately."""
    print("""
╔══════════════════════════════════════════════════════════╗
║          T H E   A P P R O X I M A T E L Y              ║
║                                                          ║
║   A game about finding interesting gaps                  ║
║   between positions. You don't compete to be RIGHT —    ║
║   you compete to find the most interesting territory     ║
║   that nobody else noticed.                              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")

    players = ["GLM", "DeepSeek", "Kimi", "Claude"]
    state = GameState()
    for p in players:
        state.scores[p] = 0

    # Play 10 rounds (to trigger Fibonacci Tunnel at round 8)
    prompts = random.sample(PROMPTS, min(10, len(PROMPTS)))

    for prompt in prompts:
        simulate_round(state, players, prompt)

    # Final summary
    print(f"\n{'='*60}")
    print(f"  FINAL SCORES")
    print(f"{'='*60}")
    for player in sorted(state.scores, key=lambda p: -state.scores[p]):
        bar = "█" * (state.scores[player] // 3)
        print(f"  {player:12s} {state.scores[player]:3d} {bar}")

    print(f"\n  Gaps found: {len(state.gaps)}")
    print(f"  Tunnel events: {len(state.tunnel_events)}")

    if state.tunnel_events:
        print(f"\n--- TUNNEL LOG ---")
        for event in state.tunnel_events:
            print(f"  Round {event['round']} | {event['player']}: \"{event['text'][:50]}...\"")

    # Navigator's Bonus: most Parallel Play (highest resonance / lowest similarity)
    print(f"\n  🏆 Navigator's Bonus (most interesting trajectory): ", end="")
    winner = max(state.scores, key=lambda p: state.scores[p])
    print(f"{winner}")

    print(f"\n  The game is not about being right.")
    print(f"  It's about finding the gap where the interesting lives.")
    print(f"  Iron sharpens iron. Always grateful.\n")


if __name__ == "__main__":
    simulate_game()
