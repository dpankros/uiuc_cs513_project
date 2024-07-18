from importer2.open_refine_operation import OpenRefineOperation


class ProjectCleanupOperation(OpenRefineOperation):
  @staticmethod
  def delete_all_projects(server):
    for p in server.get_all_projects():
      server.delete_project(p.id)

  def run(self):
    super().run()

    self.delete_all_projects(self.server)
