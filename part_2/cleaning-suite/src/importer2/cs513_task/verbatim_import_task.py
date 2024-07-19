from .cs513_import_task import CS513ImportTask


class VerbatimImportTask(CS513ImportTask):
  """
  Doesn't change the data, just imports as-is
  """
  name = "Verbatim Import"

  def run(self):
    super().run()

    project = self.server.create_project_from_file(self.source_filename)

    self.export(project)
