from .cs513_import_operation import CS513ImportOperation
from importer2.openrefine.operations import ColumnAdditionOp, TextTransformOp, OnErrorTypes


class MenuItemImportOperation(CS513ImportOperation):
  TO_ISO8601_DATE='replace(/(\\d{2,4})-(\\d{1,2})-(\\d{1,2})\\s+(\\d{1,2}):(\\d{1,2}):(\\d{1,2})\\s+UTC/, "$1$2$3T$4$5$6Z")'
  TO_ISO8601_EXTDATE='replace(/(\\d{2,4})-(\\d{1,2})-(\\d{1,2})\\s+(\\d{1,2}):(\\d{1,2}):(\\d{1,2})\\s+UTC/, "$1-$2-$3T$4:$5:$6Z")'

  def run(self):
    super().run()

    project = self.server.create_project_from_file(self.source_filename, 'MenuItem')

    notes_expression = '.'.join([
      'value',
      'trim()',
      self.NO_PAREN_QUESTION_PAREN,
      self.NO_HANGING_DELIMITER,
      self.NO_DOUBLE_SPACES,
      'trim()',
    ])

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
    # [ ] created_at
    # [ ] updated_at
    # [ ] xpos
    # [ ] ypos

    project.apply_operations([
      TextTransformOp(column_name='updated_at', expression=updated_at_expression, on_error=OnErrorTypes.STORE_ERROR).value(),
      TextTransformOp(column_name='created_at', expression=created_at_expression, on_error=OnErrorTypes.STORE_ERROR).value(),

    ])

    self.export(project)
