from .cs513_import_task import CS513ImportTask
from importer2.openrefine.operations import TextTransformOp, OnErrorTypes


class MenuItemImportTask(CS513ImportTask):
  name = "MenuItem Import"
  def run(self):
    super().run()

    project = self.server.create_project_from_file(self.source_filename, 'MenuItem')

    created_at_expression = '.'.join([
      'value',
      'trim()',
      self.TO_ISO8601_EXTDATE,
    ])

    updated_at_expression = created_at_expression

    # Columns:
    # [x] id - DNC
    # [x] menu_page_id - DNC
    # [X] price - DNC
    # [X] high_price - DNC
    # [x] dish_id -DNC
    # [x] created_at
    # [x] updated_at
    # [x] xpos - DNC
    # [x] ypos - DNC

    project.apply_operations([
      TextTransformOp(column_name='updated_at', expression=updated_at_expression, on_error=OnErrorTypes.STORE_ERROR).value(),
      TextTransformOp(column_name='created_at', expression=created_at_expression, on_error=OnErrorTypes.STORE_ERROR).value(),

    ])

    self.export(project)
