from cloudmesh.config.cm_config import cm_config_server

from cloudmesh.util.logger import LOGGER
from hostlist import expand_hostlist
from pprint import pprint
from pymongo import MongoClient
from jinja2 import Template
import sys
from cloudmesh.util.util import path_expand as cm_path_expand
from cloudmesh.config.cm_config import cm_config_server
import yaml
import json
from cloudmesh.config.cm_config import get_mongo_db
from datetime import datetime

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER('cm_mongo')

 
class ninventory:
            
    server_config = None
    
    
    def __init__(self):         
        # read the host file definition from cloudmesh_cludter.yaml
        self.server_config = cm_config_server().config
        location = cm_path_expand("~/.futuregrid/cloudmesh_cluster.yaml")
        result = open(location, 'r').read()
        template = Template(result)
        self.config = yaml.load(template.render(self.server_config))
        
        collection = "inventory"
        self.db_inventory = get_mongo_db(collection)        

    def get_attribute(self, host_label, attribute):

        try:
            value = self.find ({"cm_id" : host_label, 'cm_attribute' : 'variable', 'cm_key' : attribute})[0]
        except:
            value = None
        return value



    
    def set_attribute(self, host_label, attribute, value, time=None):
        print "SETTING", host_label, attribute, value

        if time is None:
            time = datetime.now()
        
        host = self.find_one({"cm_id": host_label, "cm_attribute":"network"})["cm_cluster"]
        
        cursor = self.update ({"cm_id" : host_label, 'cm_attribute' : 'variable', 'cm_key' : attribute},
                                  { "$set": { attribute: value,
                                             'cm_cluster': host,
                                             'cm_type': "inventory",
                                             'cm_kind': 'server',
                                             'cm_key': attribute,
                                             'cm_value': value,
                                             'cm_attribute': 'variable',
                                             'cm_refresh': time,
                                             }
                                   })

    def update(self, query, values=None):
        '''
        executes a query and updates the results from mongo db.
        :param query:
        '''
        if values is None:
            return self.db_inventory.update(query,upsert=True) 
        else:
            print query
            print values
            return self.db_inventory.update(query, values,upsert=True) 

    
    def insert(self,element):
        self.db_inventory.insert(element)

    def clear(self):
        self.db_inventory.remove({"cm_type" : "inventory"})
        
    def find(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_inventory.find(query) 
    
    def find_one(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_inventory.find_one(query) 
    
       
    def _generate_globals(self):
        
        for name in self.config["clusters"]:

            cluster = self.config["clusters"][name]
            keys = cluster.keys()
            
            element = dict({'cm_cluster': name,
                            'cm_id': name,
                            'cm_type': "inventory",
                            'cm_kind': 'server',
                            'cm_key': 'range',
                            'cm_value': expand_hostlist(cluster["id"]),
                            'cm_attribute': 'variable'
                             })
            self.insert(element)
            
            for key in keys: 
                if (type(cluster[key]) is str) and (not key in ["id","network"]):
                    element = dict({'cm_cluster': name,
                                    'cm_id': name,
                                    'cm_type': "inventory",
                                    'cm_kind': 'server',
                                    'cm_key': key,
                                    'cm_value': cluster[key],
                                    'cm_attribute': 'variable'
                             })
                    self.insert(element)
                elif key == "publickeys":
                    publickeys = cluster[key]
                    for k in publickeys:
                        element = dict({'cm_cluster': name,
                                        'cm_id': name,
                                        'cm_type': "inventory",
                                        'cm_kind': 'publickey',
                                        'cm_key': k['name'],
                                        'cm_name': cm_path_expand(k['path']), 
                                        'cm_value': cluster[key],
                                        'cm_attribute': 'variable'
                                        })
                        self.insert(element)

        
    def generate(self):    
        self._generate_globals()
        
        
        
        clusters = self.config["clusters"]
        
        for cluster_name in clusters:
            cluster = clusters[cluster_name]
            names = expand_hostlist(cluster["id"])
            net_id = 0    
            for network in cluster["network"]:
                
                n_index = expand_hostlist(network["id"])
                n_label = expand_hostlist(network["label"])
                n_range = expand_hostlist(network["range"])
                n_name = network["name"]
                
                for i in range(0,len(names)):
                    name = n_index[i]
                    element = dict(network)
                    del element['range']
                    element.update({'cm_type': "inventory",
                                     'cm_kind': 'server',
                                     'cm_id': name,
                                     'cm_cluster': cluster_name, 
                                     'id': name, 
                                     'label' : n_label[i], 
                                     'network_name': n_name, 
                                     'cm_network_id': net_id, 
                                     'ipaddr': n_range[i],
                                     'cm_attribute': 'network'}
                    )
                    self.insert(element)
                net_id +=1

        
        
    def cluster (selfself, name):
        """returns cluster data in dict"""
                 
        
    def hostlist (self, name):
        print "NAME", name
        hosts = self.find ({"cm_cluster": name, 'cm_key': 'range' })[0]['cm_value']
        print hosts
        return hosts    
                         
    
    def host (self, index, auth=True):
        cursor = self.find ({"cm_id" : index, 'cm_attribute' : 'network'})
        
        print "CCCC", cursor[0]
        
        
        data = {}
                
        data['cm_cluster'] = cursor[0]['cm_cluster']
        data['cm_type'] = cursor[0]['cm_type']  
        data['cm_id'] = cursor[0]['cm_id']  
                
        pprint (cursor[0]['cm_cluster'])
        
        c2 = self.find({"cm_attribute": 'variable'})
        
        for e in c2:
            print "EEE", e
            print
        
        cursor_attributes = self.find ({"cm_id" : index, 'cm_attribute' : 'variable'})
        for element in cursor_attributes:
            data[element['cm_key']] = element['cm_value']
        
        
        data['network']={}
        for result in cursor:
            print 70* "R"
            pprint(result)
            print 70* "S"
            
            n_id = result["cm_network_id"]
            n_name = result["network_name"]
            n_ipaddr = result["ipaddr"]
            data['network'][n_name] = dict(result)
            #del data["network"][name]["_id"]

        
        cluster_name = data['cm_cluster']
        cluster_auth = self.server_config["clusters"][cluster_name]
        
        for name in cluster_auth:
            network = data["network"][name]
            d = dict(cluster_auth[name])
            network.update(d)
            
        excludes = ['user', 'password']
        
        for name in data["network"]:
            del data["network"][name]["_id"]
            if not auth:
                for exclude in excludes:
                    if exclude in data["network"][name]:
                        del data["network"][name][exclude]
                        
        return data
                
    def ipadr (self, index, type):
        return self.find ({"cm_id": index, "type": type})[0]['ipaddr']
            
def main():
    inventory = ninventory()


    r = inventory.find ({})
    for e in r:
        print e

    print r.count()

    name = "b010"
    data = inventory.host(name)
    pprint(data)
    
    print inventory.ipadr (name, "public")
    print inventory.ipadr (name, "internal")

    
if  __name__ =='__main__':
    main()
 
