"""Copy-safe, elapsed-time based automatic blinking."""

import math
from dataclasses import dataclass, field
from random import Random


@dataclass
class BlinkController:
    """Own passive state. Time advances only while blinking is unpaused."""

    seed: int | None = None
    enabled: bool = True
    elapsed: float = 0.0
    closed: bool = False
    duration: float = 0.15
    rng: Random = field(init=False, repr=False)
    next_event: float = field(init=False)

    def __post_init__(self):
        if not math.isfinite(self.duration) or self.duration <= 0:
            raise ValueError("Blink duration must be finite and positive")
        if not math.isfinite(self.elapsed) or self.elapsed < 0:
            raise ValueError("Blink elapsed time must be finite and nonnegative")
        self.rng = Random(self.seed)
        self.next_event = self.elapsed + self.rng.uniform(2.0, 5.0)
        if self.closed:
            self.next_event = self.elapsed + self.duration

    def advance(self, dt: float) -> bool:
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("Blink dt must be finite and nonnegative")
        if not self.enabled or dt == 0:
            return self.closed
        self.elapsed += dt
        while self.elapsed + 1e-12 >= self.next_event:
            self.closed = not self.closed
            self.next_event += self.duration if self.closed else self.rng.uniform(2.0, 5.0)
        return self.closed

    def open_for_pause(self):
        """Preserve open-phase deadline; interrupt a closed phase safely."""
        if self.closed:
            self.closed = False
            self.next_event = self.elapsed + self.rng.uniform(2.0, 5.0)

    def reset_open(self):
        """Explicitly restart interval; ordinary pause/resume does not reset it."""
        self.closed = False
        self.next_event = self.elapsed + self.rng.uniform(2.0, 5.0)


def update_blink(owner, dt):
    """Operate on the updated object, never on a captured original instance."""
    if owner._expression_depth or not owner._blink_controller.enabled:
        return
    closed = owner._blink_controller.advance(dt)
    for eyelid in owner._blink_lids:
        eyelid.set_opacity(int(closed))
