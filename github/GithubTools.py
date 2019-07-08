import subprocess
import git
import utils.DirectoriesOperations
import utils.FilesOperations
import os


class GitHubTools:
    # Cargamos en variables la ruta de los script y las properties
    properties_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir + "/Files/Properties")
    script_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir + "/Files/Scripts")
    properties = utils.FilesOperations

    def create_service_list(self, clone):
        # Instanciamos el objeto propety y cargamos los valores en variables
        username = self.properties.read_properties("ScriptSection", "script.username")
        token = self.properties.read_properties("ScriptSection", "script.token")
        url = self.properties.read_properties("ScriptSection", "script.url")
        filename = self.properties.read_properties("ScriptSection", "script.filename")
        script_name = self.properties.read_properties("ScriptSection", "script.scriptname")
        if clone is True:
            subprocess.call(self.script_dir + "/" + script_name + " " + self.script_dir + " " + username +
                            " " + token + " " + url + " " + filename, shell=True)
        # Abrimos el fichero en modo lectura y vamos leyendo linea a linea el contenido del fichero
        service_file = open(self.script_dir + "\\" + filename, "r")
        service_line = service_file.readlines()
        # En funcion del tipo de servicio cambiamos el parametro enviado
        for service_type in service_line:
            if "OSB" in service_type:
                self.get_repository(GitHubTools, service_type.rstrip('\n'), "OSB")
            elif "SOA" in service_type:
                self.get_repository(GitHubTools, service_type.rstrip('\n'), "SOA")

    def get_repository(self, name_repo, dir_path):
        dir_github = self.properties.read_properties('GithubSection', 'github.path') + "\\" + dir_path
        name_repo_dir = self.properties.read_properties('GithubSection', 'github.path') + "\\" + dir_path + "\\" + name_repo
        url = self.properties.read_properties('GithubSection', 'github.endpoint') + name_repo + '.git'
        dir_operations = utils.DirectoryOperations
        # Si no existe el directorio lo creamos
        if dir_operations.check_dirs(dir_github) is False:
            dir_operations.create_dirs(dir_github)
        try:
            if dir_operations.check_dirs(name_repo_dir) is False:
                # En caso de no existir el repositorio lo clonamos
                print("clonando --> " + name_repo_dir)
                git.Git(dir_github).clone(url, b=self.properties.read_properties("GithubSection", "github.branch"))
            else:
                # Si existe el repositorio lo actualizamos
                print("Actualizando --> " + name_repo_dir)
                git.Git(name_repo_dir).pull()
        except git.exc.GitError as e:
            print("Error en a la hora de clonar/Actualizar el servicio " + name_repo_dir)
            print(str(e))
            service_error_name = "########### " + name_repo
            service_error_body = str(e)
            # Generamos un log con los repositorios que han fallado
            self.properties.create_log_error(service_error_name, service_error_body)


if __name__ == "__main__":
    GitHubTools.create_service_list(GitHubTools, False)
    # excel_simple_generator("Cibt-OSB-ManagePolicy-VS")