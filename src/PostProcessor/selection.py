import re
import yaml
from progress.spinner import Spinner
from util import StatusCodes, bcolors

class Regex:
    def __init__(self):
        #optimized and compiled regex
        self.annotations_detect = re.compile("# @[a-z|-]+: [\w|-]+")
        self.test_type_detect = re.compile("# @test-type: [\w|-]+")

    def get_compiled_regex(self, name=None):
        if name==None:
            return None
        elif name=="annotations_detect":
            return self.annotations_detect
        elif name=="test_type_detect":
            return self.test_type_detect
    

class AnnotatedDocumentHandler():
    def __init__(self, args):
        self.regex = Regex()
        f = open(args.file)
        data = str(f.read())

        try:
            with open(args.file, 'r') as file:
                
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
                self.config = yaml.load(file, Loader=yaml.FullLoader)
                self.status = StatusCodes.SUCCESS
                print(f"{bcolors.BOLD}It is a valid json file. Proceeding to check the conformity to sea specification {bcolors().ENDC}")
        except Exception as e:
            self.status = StatusCodes.ERROR
            print(f"{bcolors.FAIL}Error parsing the file. Is it in YAML format?")

        # Next read all the annotations
        self.annotations = self.regex.get_compiled_regex("annotations_detect").findall(data)
    
    def validate(self):
        #first we validate the header
        if "# @framework: SEAFramework"  not in self.annotations:
            self.status = StatusCodes.ERROR
            print(f"{bcolors().FAIL} The SEAFramework Header does not exist. Cannot proceed.")
            return False
        else:
            print(f"{bcolors().OKGREEN} SEAFramework header found. Proceeding.{bcolors().ENDC}")
        

        test = False
        for x in self.annotations:
            if self.regex.get_compiled_regex("test_type_detect").match(x):
                test = True
                break

        if not test:
            self.status = StatusCodes.ERROR
            print(f"{bcolors().FAIL} The test-type must be present. Cannot proceed.")
            return False

        # validate the sub-system should be edge or cloud.
        if "# @sub-system: edge" in self.annotations or "# @sub-system: cloud" in self.annotations:
            pass
        else:
            self.status = StatusCodes.ERROR
            print(f"{bcolors().FAIL} The sub-system should be edge or cloud. Cannot proceed.")
            return False

        return True

    def build_recommendations_to_present(self):
        # Create knowledge map
        k_tuple = {}
        for x in self.annotations:
            if x.startswith("# @sub-system:"):
                k_tuple["sub-system"] = x[15:]
            if x.startswith("# @type:"):
                k_tuple["artefact_type"] = x[9:]
            if x.startswith("# @test-type:"):
                k_tuple["test-type"] = x[14:]
        

        self.recomendations = {}

        # ToDo: connect this the DB with ORM

        if k_tuple['test-type'] == 'T01-UB':
            # First Monitoring recs
            if k_tuple['sub-system'] == "edge":
                self.recomendations['monitoring'] = ['prometheus-docker']
            elif k_tuple["sub-system"] == "cloud":
                self.recomendations['monitoring'] = ['prometheus-kubernetes', 'grafana-docker']

            #next test-profiles
            self.recomendations['test-profile'] = ["UnSecured Broker"]

            #next analytics
            self.recomendations['analytics'] = ['Unsecured-broker-analytics']

            #next iot-profiles
            self.recomendations['iot-profiles'] = ['UnsecuredBroker/bash-based']

    def present_recommendations(self):

        # Present monitoring recommendations
        print(f"{bcolors().OKBLUE} Use the monitoring artefacts : {bcolors().UNDERLINE}MonitoringArtefacts/{', '.join([str(elem) for elem in self.recomendations['monitoring']])}/{bcolors().ENDC}.")
        print(f"{bcolors().OKBLUE} Use the monitoring configurations : {bcolors().UNDERLINE}MonitoringConfigurations/{', '.join([str(elem) for elem in self.recomendations['monitoring']])}/{bcolors().ENDC}.")

        #Present the test profiles
        print(f"{bcolors().OKBLUE} Use the test profile : {bcolors().UNDERLINE}TestProfiles/{', '.join([str(elem) for elem in self.recomendations['test-profile']])}/{bcolors().ENDC}.")

        #present the analytics
        print(f"{bcolors().OKBLUE} Use the analytics : {bcolors().UNDERLINE}Analytics/{', '.join([str(elem) for elem in self.recomendations['analytics']])}/{bcolors().ENDC}.")

        #present the iot-profiles
        print(f"{bcolors().OKBLUE} Use the analytics : {bcolors().UNDERLINE}IoTProfiles/{', '.join([str(elem) for elem in self.recomendations['iot-profiles']])}/{bcolors().ENDC}.")

