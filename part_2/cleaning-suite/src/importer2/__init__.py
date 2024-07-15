from project import Project
from server import Server


if __name__ == '__main__':
    server = Server()

    # this is using a shortened version of the Dish.csv created using `cat Dish.csv| head -n 1000 > Dish_sm.csv`
    project = server.create_project_from_file('../../../data/Dish_sm.csv', 'Dish')

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

    # if desired
    # project.compute_facets('norm_name')

    # cluster on 'norm_name'
    project.cluster_column('norm_name')

    # output the UI link to this project
    print(project.get_project_url())


    def delete_all_projects(server):
        for p in server.get_all_projects():
            print(f"Deleting {p.id}:", server.delete_project(p.id))

    # delete_all_projects(server)

