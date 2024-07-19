from .timer import Timer
from .task import BaseTask
class TaskList(list, BaseTask):
  def run(self):
    overall_timer = Timer().start()
    print(f"Executing {len(self)} sequential tasks.")
    for i, task in enumerate(self):
      task_timer = Timer().start()
      print(f"- Starting {task.name}")
      task.run()
      print(f"  {task.name} ({i+1}/{len(self)}) complete. Task executed in {task_timer.stop():0.1f} seconds.\n")
    print(f"All tasks complete. Task list executed in {overall_timer.stop():0.1f} seconds.")
