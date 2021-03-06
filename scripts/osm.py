"""
Read graphs in Open Street Maps osm format

Based on osm.py from brianw's osmgeocode
http://github.com/brianw/osmgeocode, which is based on osm.py from
comes from Graphserver:
http://github.com/bmander/graphserver/tree/master and is copyright (c)
2007, Brandon Martin-Anderson under the BSD License
"""


import xml.sax
import copy
import networkx as nx
from urllib2 import urlopen


osm_url = "http://api.openstreetmap.org/api/0.6/map?bbox={},{},{},{}"
# osm_url = "http://api.openstreetmap.fr/xapi/0.6/map?*[bbox={},{},{},{}]"

nyc_poly = [[-74.00851878077059, 40.75288995157469],
            [-74.01737732563862, 40.70363450274093],
            [-74.01243283598565, 40.69988947196632],
            [-73.99782710914521, 40.70743343850899],
            [-73.97742716598874, 40.71130380771929],
            [-73.97252636835454, 40.7284549818698],
            [-73.97378303735381, 40.73527282167493],
            [-73.97213846058494, 40.74251495015199],
            [-73.942645483123, 40.77548850560436],
            [-73.9454835793063, 40.78118853872636],
            [-73.94018677228019,40.78503171212724],
            [-73.93001170688356, 40.79925356887689],
            [-73.96094552328789, 40.81318684964225]]



def download_osm(left, bottom, right, top):
    """
    Return a filehandle to the downloaded data.
    """
    param_url = osm_url.format(left, bottom, right, top)
    print param_url
    fp = urlopen(param_url)
    return fp


def read_osm(filename_or_stream, only_roads=True):
    """
    Read graph in OSM format from file specified by name or by stream object.

    Parameters
    ----------
    filename_or_stream : filename or stream object

    Returns
    -------
    G : Graph

    """

    osm = OSM(filename_or_stream)
    G = nx.DiGraph()

    for w in osm.ways.itervalues():
        if only_roads and 'highway' not in w.tags:
            continue
        G.add_path(w.nds, id=w.id, data=w)
    for n_id in G.nodes_iter():
        n = osm.nodes[n_id]
        G.node[n_id] = dict(data=n)
    return G


class Node:
    def __init__(self, id, lon, lat):
        self.id = id
        self.lon = lon
        self.lat = lat
        self.tags = {}


class Way:
    def __init__(self, id, osm):
        self.osm = osm
        self.id = id
        self.nds = []
        self.tags = {}

    def split(self, dividers):
        # slice the node-array using this nifty recursive function
        def slice_array(ar, dividers):
            for i in range(1, len(ar) - 1):
                if dividers[ar[i]] > 1:
                    left = ar[:i + 1]
                    right = ar[i:]
                    rightsliced = slice_array(right, dividers)
                    return [left] + rightsliced
            return [ar]

        slices = slice_array(self.nds, dividers)

        # create a way object for each node-array slice
        ret = list()
        for i, slice in enumerate(slices):
            littleway = copy.copy(self)
            littleway.id += "-%d" % i
            littleway.nds = slice
            ret.append(littleway)

        return ret


class OSM:
    def __init__(self, filename_or_stream):
        """ File can be either a filename or stream/file object."""
        nodes = {}
        ways = {}

        superself = self

        class OSMHandler(xml.sax.ContentHandler):
            @classmethod
            def setDocumentLocator(self, loc):
                pass

            @classmethod
            def startDocument(self):
                pass

            @classmethod
            def endDocument(self):
                pass

            @classmethod
            def startElement(self, name, attrs):
                if name=='node':
                    self.currElem = Node(attrs['id'], float(attrs['lon']), float(attrs['lat']))
                elif name=='way':
                    self.currElem = Way(attrs['id'], superself)
                elif name=='tag':
                    self.currElem.tags[attrs['k']] = attrs['v']
                elif name=='nd':
                    self.currElem.nds.append( attrs['ref'] )

            @classmethod
            def endElement(self,name):
                if name=='node':
                    nodes[self.currElem.id] = self.currElem
                elif name=='way':
                    ways[self.currElem.id] = self.currElem

            @classmethod
            def characters(self, chars):
                pass

        xml.sax.parse(filename_or_stream, OSMHandler)

        self.nodes = nodes
        self.ways = ways

        #count times each node is used
        node_histogram = dict.fromkeys( self.nodes.keys(), 0 )
        for way in self.ways.values():
            if len(way.nds) < 2:       #if a way has only one node, delete it out of the osm collection
                del self.ways[way.id]
            else:
                for node in way.nds:
                    node_histogram[node] += 1

        #use that histogram to split all ways, replacing the member set of ways
        new_ways = {}
        for id, way in self.ways.iteritems():
            split_ways = way.split(node_histogram)
            for split_way in split_ways:
                new_ways[split_way.id] = split_way
        self.ways = new_ways
