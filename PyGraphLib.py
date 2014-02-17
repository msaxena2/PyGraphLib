'''
Created on Sep 26, 2013

Graph library to create a graph
directional graphs with weighted/un-weighted edges
and non directional graphs can be created

@author: Manasvi
'''
from operator import itemgetter
from Queue import PriorityQueue
import sys
#Constants defining error codes
KEY_NOT_FOUND_ERROR = 'key not present in graph'
OPERATION_SUCCESSFUL = 'success'
NODE_NOT_PRESENT_ERROR = 'node not found in graph'
DIRECT_PATH_FOUND = 'direct path found'
PATH_NOT_FOUND = 'path not found'
NODES_NOT_CONNECTED = 'nodes not connected'
PATH_NOT_PRESENT = 'direct path not present'
#constants defining values
MAX_NUM = sys.maxint
KEY_INDEX = 1
PRIORITY_INDEX = 0

class graph:
    #instance variables
    data_dict = dict()                      #holds the data associated with every node
    graph_connections_dict = dict()              #holds the data associated with every edge
        
        
    def add_new_node(self, node_key, node_data):
        '''
        Adds a new node to the dictionary
        
        @param node_key: node_key: key of new node
        @param node_data: data associated with node
        @return: status of the operation
        '''
        self.data_dict[node_key] = node_data
        self.graph_connections_dict[node_key] = dict()
        return OPERATION_SUCCESSFUL
        
    def add_connection(self, origin_node_key,
                       destination_node_key, edge_weight):
        '''
        Adds connection between the specified nodes
        @param origin_node_key: origin_node_key: key of origin node
        @param destination_node_key: destination_node_key: key of destination node
        @return: status of operation
        
        ''' 
        if origin_node_key not in self.data_dict \
            or destination_node_key not in self.data_dict:
            return NODE_NOT_PRESENT_ERROR;
        node_specific_dict = self.graph_connections_dict[origin_node_key]
        node_specific_dict[destination_node_key] = edge_weight
        return OPERATION_SUCCESSFUL
            
    
    def get_node_data(self, node_key):
        '''
        Gets the data associated with the node
        @param node_key: key of the node
        @return: data of the node or error message if node not found
        '''
        if node_key not in self.data_dict:
            return KEY_NOT_FOUND_ERROR
        return self.data_dict[node_key]    
    
    
    def is_direct_path_present(self, origin_node, destinaiton_node):
        '''
        check whether direct path exists between two nodes
        @param origin_node: key of the origin node
        @param destination_node: Key of the destination node
        @return: Success or error codes
        ''' 
        if origin_node not in self.data_dict \
            or destinaiton_node not in self.data_dict:
            return NODE_NOT_PRESENT_ERROR
        conList = self.graph_connections_dict[origin_node]
        if destinaiton_node in conList:
            return DIRECT_PATH_FOUND
        return PATH_NOT_FOUND
    
   
    def get_path_weight(self, origin_node, destination_node):
        '''
        gets the weight of path associated with specified origin node
        @param origin_node: Key of the origin node
        @return: Weight or error code
        '''
        if origin_node not in self.data_dict \
            or destination_node not in self.data_dict:
            return NODE_NOT_PRESENT_ERROR
        con_list = self.graph_connections_dict[origin_node]
        if destination_node in con_list:
            return con_list[destination_node]
        return PATH_NOT_FOUND
    
    def get_all_data(self):
        '''
        return all data in the graph in the form of a list
        '''
        return_val = list()
        for key in self.data_dict:
            return_val.append(self.data_dict[key])
        return return_val
    
    def get_all_neighbors(self, node_key):
        '''
        return all the neighbor nodes' keys
        @param node_key: key of origin node
        @return: List of all neighbors' keys and weights
        '''
        if node_key not in self.graph_connections_dict:
            return KEY_NOT_FOUND_ERROR
        return_val = self.graph_connections_dict[node_key]
        return_list = list()
        for val in return_val:
            neighbor_key = val
            edge_weight = return_val[neighbor_key]
            temp_list = [neighbor_key, edge_weight]
            return_list.append(temp_list)
        return return_list
    
    def get_sorted_data_list(self):
        '''
        returns all data in list sorted by key
        '''
        return_list = list();
        for node_key in self.graph_connections_dict:
            temp_dict = self.graph_connections_dict[node_key]
            for neighbor_key in temp_dict:
                temp_list = [node_key, neighbor_key, 
                             temp_dict[neighbor_key]]
                return_list.append(temp_list)
        sorted_return_list = sorted(return_list, key=itemgetter(2))
        return sorted_return_list      
    
    def get_cheapest_edge(self):
        '''
        return the cheapest edge i.e. edge with minimum weight
        '''
        data_list = self.get_sorted_data_list()
        return data_list[0];
   
    def get_costliest_edge(self):
        '''
        returns costliest edge i.e. edge with most weight
        '''
        data_list = self.get_sorted_data_list()
        return data_list[-1];
    
    def get_average_edge_cost(self):
        ''' 
        returns the average weight of all edges
        '''
        data_list = self.get_sorted_data_list();
        edge_sum = 0 
        edge_count = 0
        for temp_list in data_list:
            edge_sum += temp_list[2]
            edge_count  += 1
        return edge_sum / edge_count
    
    def get_nodelist_by_degree(self):
        '''
        return a list of nodes sorted by degrees
        '''
        degree_dict = dict()
        for node_key in self.graph_connections_dict:
            degree = len(self.graph_connections_dict[node_key])
            degree_dict[node_key] = degree
        final_list = sorted(degree_dict, key=degree_dict.__getitem__, reverse=True)
        return final_list
        
        
    def remove_node(self, node_key):
        '''
        Removes the specified node from the graph. Also removes the connections
        associated with the node
        
        @param node_key: the key of the node to be removed
        @return : Status message of the operation
        '''
        if node_key not in self.data_dict or node_key not in self.graph_connections_dict:
            return KEY_NOT_FOUND_ERROR
        del self.graph_connections_dict[node_key]
        for key in self.graph_connections_dict:
            connections_dict = self.graph_connections_dict[key]
            for neighbor in connections_dict:
                if neighbor == node_key:
                    del connections_dict[node_key]
                    break
        del self.data_dict[node_key]
        return OPERATION_SUCCESSFUL
    
    def remove_connection(self, origin_node_key, destination_node_key):
        '''
        Removes the connection between the specified origin node and the specified destination node
        Keep in mind that this only removes the connection in one direction, for undirected graphs, 
        the function must be called again with the destination node as the origin node and origin node as the
        destination node
        
        @param origin_node_key: the key of the origin node
        @param destination_node_key: the key of the destination node
        @return: status of the operation
        '''
        if origin_node_key not in self.data_dict or origin_node_key not in self.graph_connections_dict:
            return KEY_NOT_FOUND_ERROR
        if destination_node_key not in self.data_dict or destination_node_key not in self.graph_connections_dict:
            return KEY_NOT_FOUND_ERROR
        if destination_node_key not in self.graph_connections_dict[origin_node_key]:
            return NODES_NOT_CONNECTED
        del self.graph_connections_dict[origin_node_key][destination_node_key]
        return OPERATION_SUCCESSFUL
    
        
        
    def print_dict(self):
            print self.graph_connections_dict
            print self.data_dict
            
        
    def get_degree(self, node_key):
        '''
        Returns The number degree of specified node
        @param node_key: The key of the node for finding the degree
        @return: The degree or error code
        '''
        if node_key not in self.graph_connections_dict \
        or node_key not in self.data_dict:
            return KEY_NOT_FOUND_ERROR
        return len(self.graph_connections_dict[node_key]) 
    
    def get_shortest_path(self, origin_key, destination_key):
        '''
        Uses Djikstra's shortest path algorithm to return the shortest path
        between the specified nodes
        
        @param origin_key: The key of the origin node
        @param destinaiton_key: The key of the destination node
        @return: The path in the form of an array or path not found error
        '''
        
        path_dict = dict()
        unvisited_list = list()
        visited_list = list()
        if origin_key not in self.data_dict or destination_key not in self.data_dict:
            return KEY_NOT_FOUND_ERROR
        for node_key in self.data_dict:
            if node_key == origin_key:
                unvisited_list.append((node_key, 0))
            else:
                unvisited_list.append((node_key, sys.maxint))
        unvisited_list = sorted(unvisited_list, key=itemgetter(1))    
        while len(unvisited_list) != 0:
            tup = unvisited_list.pop(0)
            current_node = tup[0]
            current_priority = tup[1]
            visited_list.append(current_node)
            if current_node == destination_key:
                break
            if current_priority == sys.maxint:
                break;
            for neighbor_node in self.graph_connections_dict[current_node]:
                if neighbor_node not in visited_list:
                    for index in range(0, len(unvisited_list)):
                        if neighbor_node == unvisited_list[index][0]:
                            break
                    neighbor_priority = unvisited_list[index][1]
                    if (self.get_path_weight(current_node, neighbor_node) + current_priority) < neighbor_priority:
                        unvisited_list[index] = (neighbor_node, self.get_path_weight(current_node, neighbor_node) + current_priority)
                        unvisited_list = sorted(unvisited_list, key=itemgetter(1))
                        path_dict[neighbor_node] = current_node
        path_list = list()
        path_list.append(destination_key)
        search_node = destination_key
        while True:
            if search_node not in path_dict:
                return PATH_NOT_PRESENT
            search_node = path_dict[search_node]
            path_list.append(search_node)
            if search_node == origin_key:
                path_list.reverse()
                return path_list
    

    

        
            
            