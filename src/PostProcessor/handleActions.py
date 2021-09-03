import yaml
import time
from progress.spinner import Spinner
from tabulate import tabulate
from ContextProcessor import MongoContextProcessor
from ArtefactProcessor import MongoArtefactProcessor
from ArtefactInstanceProcessor import DockerArtefactInstanceProcessor
from util import StatusCodes, bcolors


# Gets configuration for the suite
def get_configuration(args):
    spinner = Spinner(f'{bcolors.WARNING}Parsing Configuration ')

    # Easter Egg! Not really required
    count = 0
    while count < 10:       
        time.sleep(0.1)
        count = count + 1
        spinner.next()
    spinner.finish()

    

    
class ActionMethods:
    @staticmethod
    def get_database_connector(config, type_of_client = "artefact"):
        database_params = config["database"]
        
        if database_params["type"] != "mongodb":
            print(f"{bcolors.FAIL}Only MongoDb is supported for now!")
            return StatusCodes.ERROR
        
        if type_of_client == "artefact":
        # ToDo handle username/password = null
            return MongoArtefactProcessor.ArtefactProcessor( database_params["address"], 
                                                    database_params["port"], 
                                                    organization_name = config["organization"], 
                                                    uname=database_params["username"], 
                                                    psswd=database_params["password"])

        return MongoContextProcessor.ContextProcessor( database_params["address"], 
                                                    database_params["port"], 
                                                    organization_name = config["organization"], 
                                                    uname=database_params["username"], 
                                                    psswd=database_params["password"])
        

class CreateAction:
    @staticmethod
    def handle_create(args):
        # It has become almost a boilerplate code :(
        status, config = get_configuration(args)

        if status == StatusCodes.ERROR:
            print(f"ERROR: {config}")
            return

        if args.type=="artefact":
            db_client = ActionMethods.get_database_connector(config)
            status, msg = db_client.create_artefact(args.name, args.context, args.layer, args.path, args.expose)
            print(msg)

        else:
            if ":" in args.name:
                print(f"{bcolors.FAIL}Using a colon(:) in context name is not allowed")
                return
            db_client = ActionMethods.get_database_connector(config, "context")            
            status, msg = db_client.create_context(args.name)
            print(msg)


class DeleteAction:
    @staticmethod
    def handle_delete(args):
        # It has become almost a boilerplate code :(
        status, config = get_configuration(args)

        if status == StatusCodes.ERROR:
            print(f"ERROR: {config}")
            return

        if args.type=="artefact":
            db_client = ActionMethods.get_database_connector(config)
            status, msg = db_client.delete_artefact(args.name, args.context, args.layer)
            print(msg)

        else:
            db_client = ActionMethods.get_database_connector(config, "context")            
            status, msg = db_client.delete_context(args.name)
            print(msg)


class RunAction:
    @staticmethod
    def handle_run(args):
        status, config = get_configuration(args)

        if status == StatusCodes.ERROR:
            print(f"ERROR: {config}")
            return

        db_client = ActionMethods.get_database_connector(config)
        queue_params = config["queue-processor"]

        if queue_params["type"] != "redis":
            print(f"{bcolors.FAIL}Only Redis as quque-processor is supported for now!")
            return 

        docker_client = DockerArtefactInstanceProcessor.DockerArtefactProcessor(queue_params)

        if args.stop == False:
            RunAction.handle_create(args, db_client, docker_client)
        else:
            RunAction.handle_stop(args, docker_client)                
            

    @staticmethod
    def handle_create(args, db_client, docker_client):
        status, data = db_client.get_artefacts_data(args.context, args.layer)

        if status == StatusCodes.ERROR:
            print(data)
            return
        
        status, msg = docker_client.run_artifact(data)
        print(msg)

    @staticmethod
    def handle_stop(args, docker_client: DockerArtefactInstanceProcessor):
        status, msg = docker_client.stop_artifacts(args.context, args.layer)
        print(msg)
        return


class ShowAction:
    @staticmethod
    def handle_show(args):
        # It has become almost a boilerplate code :(
        status, config = get_configuration(args)

        if status == StatusCodes.ERROR:
            print(f"ERROR: {config}")
            return

        if args.type == 'current':
            queue_params = config["queue-processor"]

            if queue_params["type"] != "redis":
                print(f"{bcolors.FAIL}Only Redis as queue-processor is supported for now!")
                return 

            docker_client = DockerArtefactInstanceProcessor.DockerArtefactProcessor(queue_params)
            status, data = docker_client.find_running_artefacts(args.context)

            if status == StatusCodes.ERROR:
                print(f"{bcolors.FAIL} Oops! Some error occured")
                return

            #Enable bold tables
            print(f"{bcolors.ENDC}{bcolors.BOLD}")
            print(tabulate(data, headers = ['layer', 'context', 'artefact_name', 'id']))
        else:
            pass