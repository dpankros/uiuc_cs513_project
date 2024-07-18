from .cs513_import_operation import CS513ImportOperation


class DishImportOperation(CS513ImportOperation):
  def run(self):
    super().run()
    source_filename = self.config['source_filename']
    dest_filename = self.config['dest_filename']
    server_url = self.config['server_url']
    sql_engine = self.config['sql_engine']

    assert source_filename, "source_filename is required"
    assert dest_filename, "dest_filename is required"

    server = self.server

    # this is using a shortened version of the Dish.csv created using `cat Dish.csv| head -n 1000 > Dish_sm.csv`
    project = server.create_project_from_file(source_filename, 'Dish')

    op = [
      {
        "op": "core/column-addition",
        "engineConfig": {
          "facets": [],
          "mode": "row-based"
        },
        "baseColumnName": "name",
        "expression": 'grel:value.trim().toLowercase().replace(\" & \",\" and \").replace(/[\\;\\:\\.\\,\\>\\<\\/\\?\\[\\]\\{\\}\\(\\)\\*\\&\\^\\%\\$\\#\\@\\!\\-\\+\\=\\_]/, \"\")',
        "onError": "set-to-blank",
        "newColumnName": "norm_name",
        "columnInsertIndex": 2,
        "description": "Create column norm_name"
      }

    ]
    # create the norm_name column
    project.apply_operations(op)

    # cluster on 'norm_name'
    project.cluster_column('norm_name')

    self.export(project)
