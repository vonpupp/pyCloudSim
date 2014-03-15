#!/usr/bin/env python
'''Clustering

Based on 
V.D. Blondel, J.-L. Guillaume, R. Lambiotte and E. Lefebvre (2008). "Fast unfolding of community hierarchies in large networks". J. Stat. Mech. 2008 (10): P10008. doi:10.1088/1742-5468/2008/10/P10008
'''
__date__='June 2013'
__version__='1.1'
__author__='Vincent Van Asch'

import os, sys, getopt, time
import pickle
from math import pow

def loginfo(s): print >>sys.stderr, '%s: %s' %(time.strftime('%d/%m/%Y %H:%M:%S'), s)


def fread(fname, sep=None):
    try:
        f = open(os.path.abspath(os.path.expanduser(fname)), 'rU')
        for l in f:
            line = l.strip()
            if line:
                yield line.split(sep)
    finally:
        f.close()


class World(dict):
    def __init__(self, d={}, depth=None):
        dict.__init__(self, d)
        self._depth = None
        
    @property
    def depth(self):
        '''The number of levels'''
        if self._depth is None:
            self._depth = getdepth(self)
        return self._depth

    def level(self, n):
        '''Get the communties as lists (expressed in original vertices)
        at level n (ranging from 0 to depth)'''
        if n > self.depth or n < 0: raise ValueError('Non existing level')        
        
        pool=[self]
        depth = self.depth
        step=0
        if n != 0:
            # Get the required resolution
            while step <= n:
                newpool=[]
                for p in pool:
                    if step == self.depth:
                        newpool.extend(p)
                    else:
                        newpool.extend(p.values())
                step+=1

                pool = newpool[:]

        if n != self.depth:
            # Expand
            data=[]
            for p in pool:
                subpool = [p]
                while isinstance(subpool[0], dict):
                    newsubpool=[]
                    for sp in subpool:
                        newsubpool.extend(sp.values())
                    subpool = newsubpool[:]
                newsubpool=[]
                for sp in subpool:
                    newsubpool.extend(sp)
                data.append(newsubpool)
        else:
            # Each element in its group
            data = [[x] for x in pool]
        
        # sort
        [x.sort() for x in data]
        data.sort(key=lambda x:x[0])
        
        return data
            
            

class Network(dict):
    def __init__(self, d={}, id=None):
        dict.__init__(self, d)
        self._communities={}
        self._revcommunities={}
        self._total=0
        self._id = id
        
    @property
    def id(self):
        '''the network id'''
        if self._id is None: raise ValueError('id has not been set')
        return self._id
        
    def add_edge(self, v1, v2, w=1, add=False):
        '''Adds the edge between vertex v1 and vertex v2 and puts the weight w
        on the edge.
        
        The edge is non-directional.
        
        w: the weight for the edge
        
        add: if False, the edge gets weight w; if True the value w
             is added to the weight if the edge is already present in 
             the network.
        '''
        try:
            self[v1]
        except KeyError:
            self[v1] = {v2:w}
        else:
            if add:
                self[v1][v2] = self[v1].get(v2, 0) + w
            else:
                self[v1][v2] = w
        self._total+=1
        
        # The reverse
        try:
            self[v2]
        except KeyError:
            self[v2] = {v1:w}
        else:
            if add:
                self[v2][v1] = self[v2].get(v1, 0) + w
            else:
                self[v2][v1] = w
            
        
    def __len__(self):
        '''The number of edges in the Network'''
        return self._total

    @property
    def vertices(self):
        '''A list containing all vertices'''
        pool = self.keys()
        pool.sort()
        return pool[:]

    def edge(self, v1, v2):
        '''Returns the weight of the edge between v1 and v2.
        
        If no edge returns 0'''
        try:
            return self[v1][v2]
        except KeyError:
            return 0
        
    def size(self, genre):
        '''
        If genre == "vertex": returns number of vertices
        If genre == "edge"  : returns number of edges
        If genre == "community"  : returns number of non-empty communities
        '''
        if genre == "edge":
            return len(self)
        elif genre == "vertex":
            return len(self.vertices)
        elif genre == "community":
            count=0
            for c, members in self._revcommunities.items():
                if members: count+=1
            return count
            
    def weight(self, v=None):
        '''Returns the sum of all edges attached to vertex v.
        
        If v is None, it returns the sum of all edge weights
        '''
        if v is None:
            total = 0
            for k in self.vertices:
                total += self.weight(k)
            return total
        
        try:
            self[v]
        except KeyError:
            raise KeyError('vertex "%s" not in network' %(str(v)))
        else:
            total = sum(self[v].values())
           
        return total
        
    def adjacency(self):
        '''Prints the adjacency matrix'''
        out = ['\t'.join(['']+[str(x) for x in self.vertices])]
        for v1 in self.vertices:
            line=[str(v1)]
            for v2 in self.vertices:
                line.append(str(self.edge(v1, v2)))
            out.append('\t'.join(line))
        print '\n'.join(out)
        
    def edges(self):
        '''All edges in the network as a list of tuples: (v1, v2, w)'''
        count=0
        for i, v1 in enumerate(self.vertices):
            for v2 in self.vertices[i:]:
                edge = self.edge(v1, v2)
                if edge:
                    yield v1, v2, edge
                    count+=1
            
        #if count != self.size("edge"):
        #    raise ValueError('missed edges: %d <> %d' %(count, self.size("edge")))
            
            
    def dump(self, fname):
        '''Dumps the network to a file in the format:
            vertex1   vertex2   weight
        '''
        try:
            f = open(os.path.abspath(os.path.expanduser(fname)), 'w')
            count=0
            for e in self.edges():
                f.write('%s\t%s\t%s\n' %e)
                count+=1
        finally:
            f.close()
        #loginfo('Written %d edges to %s' %(count, fname))
        
    def getcommunity(self, v):
        '''Returns the communities for vertex v'''
        return self._communities[v]
    
    def setcommunity(self, v, c):
        '''Puts vertex v in community c'''
        try:
            self._communities[v]
        except KeyError:
            self._communities[v] = []
        try:
            self._revcommunities[c]
        except KeyError:
            self._revcommunities[c] = []
            
        if c not in self._communities[v]:
            self._communities[v].append(c)
            self._revcommunities[c].append(v)
            
    def delcommunity(self, v, c):
        '''Remove vertex v from community c'''
        if c in self._communities[v]:
            self._communities[v].remove(c)
            self._revcommunities[c].remove(v)
            
    def community(self, c):
        '''Returns a list of all vertices in community c'''
        return self._revcommunities[c]
    def move(self, v, c1, c2):
        '''Move vertex v from c1 to c2'''
        if c1 not in self.getcommunity(v): raise ValueError('vertex not in community %s' %str(c1))
        if c2 in self.getcommunity(v): raise ValueError('vertex already in community %s' %str(c2))
        
        self.delcommunity(v, c1)
        self.setcommunity(v, c2)
        
        
    def delta(self, v1, v2):
        '''Returns 1 if v1 is in the same community as v2;
        otherwise 0'''
        if set(self.getcommunity(v1)).intersection(set(self.getcommunity(v2))):
            return 1
        return 0
        
        
    @property
    def modularity(self):
        '''Returns the modularity value'''
        return modularity(self)


    def difference(self, v, c):
        '''The modularity difference when vertex v would be moved
        from its own singular community into community c'''
        m = 0.5*self.weight()
        
        # All vertices in c
        vertices = self.community(c)[:]
        try:
            vertices.remove(v)
        except Exception:
            pass
        
        # Sum of weights of links inside c
        sum_in = 0.0
        for i in vertices:
            for j in vertices:
                sum_in += self.edge(i, j)
                
        # Sum of weights of links incident to vertices in c
        sum_tot = 0.0
        for i in vertices:
            sum_tot += self.weight(i)

        # Sum of weights of links incident to v
        k = self.weight(v)

        # Sum of weights of links between v and other vertices in c
        k_in = 0.0
        for i in vertices:
            k_in += self.edge(v, i)

        # Combine
        A = (sum_in + 2.0*k_in)/(2*m) - pow((sum_tot+k)/(2*m), 2)
        B = sum_in/(2*m) - pow(sum_tot/(2*m), 2) - pow(k/(2*m), 2)
        return A - B
        

    def switch(self, v, c1, c2):
        '''Returns the modularity difference when vertex v
        is moved from community c1 to c2.
        
        If positive the modularity increases with the move
        '''
        # Moving out
        A = self.difference(v, c1)
        # Moving in
        B = self.difference(v, c2)
        return B - A 



def modularity(n):
    '''Return the modularity value of a network with communities'''
    m = 0.5*n.weight()
    total=0.0
    for v1 in n.vertices:
        for v2 in n.vertices:            
            if n.delta(v1, v2):
                k1 = n.weight(v1)
                k2 = n.weight(v2)
                A12 = n.edge(v1, v2)
         
                total += ( A12 - (k1*k2/(2*m)) )
                    
    return total / (2*m)
                
    
    
def phase1(n, t=0, verbose=False):
    '''Puts each node (in a singular community) into the community
    that leads to the highest modularity gain. Return the network n
    when modularity gain does no longer exceed threshold t'''
    moves=True
    loops=0
    while moves:
        moves=0
        for v in n.vertices:
            # For all neighbors
            maxgain = None
            c1 = n.getcommunity(v)[0]
            for neighbor, w in n[v].items():
                c2 = n.getcommunity(neighbor)[0]
                #print v, neighbor, c1, c2
                if c1 == c2: continue
                q = n.switch(v, c1, c2)
            
                if maxgain is None or q > maxgain[1]:
                    maxgain = c2, q
            
            # check if we move
            if maxgain is not None and maxgain[1] > t:
                n.move(v, c1, maxgain[0])
                moves+=1
        loops+=1
        if verbose: loginfo('Loop %d: Moved %d out of %d vertices' %(loops, moves, n.size("vertex")))
        
        
    # Remove empty communities
    data =  n._revcommunities.items()[:]
    for c, members in data:
        if not members:
            n._revcommunities.pop(c)
        
    if 0: 
        for c in n._revcommunities.keys():
            print >>sys.stderr, 'community', c, n.community(c) 
        
    return n
    
def phase2(n, verbose=False):
    '''Community aggregation'''
    m = Network()
    
    for c1, members1 in n._revcommunities.items():
        # Sum of weights of links inside c1
        sum_in = 0
        for i in members1:
            for j in members1:
                sum_in += n.edge(i, j)
        m.add_edge(c1, c1, sum_in)
        
        # Get all edges to the other communities
        for c2, members2 in n._revcommunities.items():
            sum_out = 0
            if c1 != c2:
                for i in members1:
                    for j in members2:
                        sum_out+=n.edge(i, j)
                m.add_edge(c1, c2, sum_out)

    # Each vertex in its own community
    for v in m.vertices:
        m.setcommunity(v,v)

    return m
    

def getdepth(d):
    depth=1
    l = d[d.keys()[0]]
    while isinstance(l, dict):
        depth+=1
        l = l[l.keys()[0]]
    return depth

def expand(members, history, depth):
    if len(history) + depth >= 0:
        h = history[depth]
    
        out={}
        for key, m in enumerate(members):
            out[key] = expand(h[m], history, depth-1)
    else:
        return members
            
    return out

def louvainmethod(n, verbose=False, maximum=None):
    '''Takes a Network and returns the communities on different levels.
    
    Does not change the original network.
    
    maximum: limit to the number of passes to maximum
    '''
    # Info
    if verbose: 
        loginfo('Looking for communities in network with %d vertices and %d edges' %(n.size("vertex"), n.size("edge")))
        if maximum is not None: loginfo('The number of passes is limited to %d' %maximum)
    
    history=[]
    passes = 1
    
    # Put each vertex in its own community
    network = Network(d=n)
    
    while 1:
        if verbose: loginfo('=== Processing pass %d...' %passes)
        for v in network.vertices:
            network.setcommunity(v,v)
        
        # Phase 1: Modularity optimization
        network = phase1(network, verbose=verbose)
        
        # Keep the history
        history.append(network._revcommunities)
        
        # Phase 2: Community aggregation
        supernetwork = phase2(network, verbose=verbose)
        
        passes+=1
        
        if network == supernetwork: break
        
        network = Network(d=supernetwork)
        
        if maximum is not None:
            if passes > maximum: break
        
    # Merge the history
    out=expand(history[-1].keys(), history, depth=-1)
 
    return World(out)
    
    
def example():
    '''Returns an example Network.
    The example comes from Figure 1 in the Blondel et al. (2008) paper'''
    n = Network()
    #for v1, v2 in [(1,2),(1,3),(1,10),(2,3),(4,5),(4,6),(4,10),(5,6),(7,8),(7,9),(7,10),(8,9)]:
    #for v1, v2 in [(1,5), (2,3), (2,4), (2,5), (3,5)]:
    for v1, v2 in [(0,2),(0,3),(0,4),(0,5),(1,2),(1,4),(1,7),(2,4),(2,5),(2,6),(3,7),(4,10),(5,7),(5,11),(6,7),(6,11),
                   (8,9),(8,10),(8,11),(8,14),(8,15),(9,12),(9,14),(10,11),(10,12),(10,13),(10,14),(11,13)]: 
        n.add_edge(v1, v2, 1)

    #print n
    #print n.size("edge"), 'edges'
    #print n.size("vertex"), 'vertices'
    #print 'sum Aij:', n.weight()
    
    #for v in n.vertices:
    #    print v, ':', n.weight(v)
   
    # Singular communities
    #for v in n.vertices:
    #    n.setcommunity(v, v)
    #print n.size("community"), 'non-empty communities'
      
    '''
    n.setcommunity(1, 1)
    n.setcommunity(2, 1)
    n.setcommunity(3, 1)
    n.setcommunity(7, 2)
    n.setcommunity(8, 2)
    n.setcommunity(9, 2)
    n.setcommunity(4, 3)
    n.setcommunity(5, 3)
    n.setcommunity(6, 3)
    n.setcommunity(10, 1)
'''

    #for c in n._revcommunities.keys():
    #    print 'community', c, n.community(c) 
    
    #pre = n.modularity
    #print 'MODULARITY', pre    
    #print 'SWITCH', n.switch(10, 2, 3)

    return n



def file2network(fname):
    '''Reads in a file and returns a Network'''
    n = Network(id=fname)
    for line in fread(fname):
        if len(line) >= 2:
            v1 = line[0]
            v2 = line[1]
            w = 1
            
            try:
                v1 = int(v1)
            except ValueError:
                pass
            try:
                v2 = int(v2)
            except ValueError:
                pass
            
        if len(line) == 3:
            w = float(line[2])
        if len(line) not in [2,3]: raise ValueError('Wrong format: %s' %str(line))
    
        n.add_edge(v1, v2, w)
        
    return n
    



def compute(fname, verbose=True, level=None, dump=False, maximum=None):
    '''Takes a file with and prints all levels'''
    n = file2network(fname)

    if dump:
        name1= fname+'.network.pcl'
        f=open(name1, 'w')
        pickle.dump(n, f)
        f.close()

    c = louvainmethod(n, verbose, maximum=maximum)

    if dump:
        name2=fname+'.world.pcl'
        f=open(name2, 'w')
        pickle.dump(dict(c), f)
        f.close()
        loginfo('Written %s and %s' %(name1, name2))
    
    for l in range(c.depth, -1, -1):
        if level is None or level == c.depth-l:
            if verbose:
                plural = 'ies'
                if len(c.level(l)) == 1: plural='y'
                print >>sys.stderr, '+++ LEVEL %d (%4d communit%-3s) +++' %(c.depth-l, len(c.level(l)), plural)
            for i,comm in  enumerate(c.level(l)):
                #if verbose: print >>sys.stderr, 'COMMUNITY %d with %d member(s):' %(i, len(comm))
                print '\t'.join(comm)
            print
    



def _usage():
    print >>sys.stderr, '''Find communities in a graph (version %s)
    
USAGE
    $ python louvain.py [-d] [-v] [-m int] [-l level] file
    
    file: A file with edges.
    
    Print the communities to STDOUT.
    Each community as a tab-separated list of vertices.
    Each level is separated by an empty line.
    
    
OPTIONS
    -v: Print more information
    -l level: level should be an integer. When given, only
              this level is printed.
    -d: Dump the network and the community structure to pickled files.
        The community structure is dumped as a dictionary.
    -m int  : the script starts with each vertex in its own community and ends
              with 1 community containing all vertices (level 0). The -m option
              sets the maximum level for the end point. 
    
FORMAT
    The a line in inputfile should look like:
    
        vertex1  vertex2
    
    Which means that there is an edge from vertex1 to vertex2.
    The direction is not important.
    
    Additionally, a weight can be specified:
    
        vertex1 vertex2 0.5
    
    A vertex name cannot contain whitespace.
    
    
REFERENCE
    V.D. Blondel, J.-L. Guillaume, R. Lambiotte and E. Lefebvre (2008). "Fast unfolding of community hierarchies in large networks". J. Stat. Mech. 2008 (10): P10008.

%s, %s
'''%(__version__, __author__, __date__)
    
    
if __name__ == '__main__':        
    try:
        opts,args=getopt.getopt(sys.argv[1:],'hvl:dm:', ['help'])
    except getopt.GetoptError:
        # print help information and exit:
        _usage()
        sys.exit(2)

    verbose=False
    level=None
    dump=False
    maximum = None
    
    for o, a in opts:
        if o in ('-h', '--help'):
            _usage()
            sys.exit()
        if o == '-v':
            verbose=True
        if o == '-l':
            level=int(a)
        if o == '-d':
            dump=True
        if o == '-m':
            maximum = int(a)

    if len(args) != 1:
        _usage()
        sys.exit(1)
        
    fname = args[0]
        
    compute(fname, verbose=verbose, level=level, dump=dump, maximum=maximum)

    