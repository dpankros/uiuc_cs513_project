from .open_refine_task import OpenRefineTask
from importer2.openrefine import Server


class ProjectCleanupTask(OpenRefineTask):
  name = "OpenRefine Project Cleanup"
  @staticmethod
  def delete_all_projects(server: Server):
    for p in server.get_all_projects():
      server.delete_project(p.id)  # type: ignore

  def run(self):
    super().run()

    self.delete_all_projects(self.server)
