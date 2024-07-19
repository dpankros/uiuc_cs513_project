from .cs513_import_task import CS513ImportTask


class MenuPageImportTask(CS513ImportTask):
  name = "MenuPage Import"

  def run(self):
    super().run()

    project = self.server.create_project_from_file(self.source_filename, 'MenuPage')

    # Columns:
    # [x] id - DNC
    # [x] menu_id - DNC
    # [x] page_number - DNC
    # [x] image_id - DNC
    # [x] full_height - DNC
    # [x] full_width - DNC
    # [x] uuid - DNC

    self.export(project)
