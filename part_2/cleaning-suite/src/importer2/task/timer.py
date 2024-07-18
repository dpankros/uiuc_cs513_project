import time

class TimerError(Exception):
  """A custom exception used to report errors in use of Timer class"""

class Timer:
  def __init__(self):
    self._start_time = None
    self._end_time = None

  def start(self):
    """Start a new timer"""
    if self._start_time is not None:
      raise TimerError(f"Timer is running. Use .stop() to stop it")

    self._end_time = None
    self._start_time = time.perf_counter()
    return self

  def stop(self):
    """Stop the timer, and report the elapsed time"""
    if self._start_time is None:
      raise TimerError(f"Timer is not running. Use .start() to start it")

    self._end_time = time.perf_counter()
    return self.elapsed_time

  def reset(self):
    """Reset the timer"""
    self._start_time = None
    self._end_time = None
    return self

  @property
  def elapsed_time(self):
    return self._end_time - self._start_time

  @property
  def start_time(self):
    return self._start_time

  @property
  def end_time(self):
    return self._end_time
