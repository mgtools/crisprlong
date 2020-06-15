// A C++ program to print topological sorting of a DAG
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <string>
#include <cstring>
#include <list>
#include <stack>
using namespace std;

// Class to represent a graph
class Graph
{
	int V; // No. of vertices'

	// Pointer to an array containing adjacency listsList
	list<int> *adj;

	// A function used by topologicalSort
	void topologicalSortUtil(int v, bool visited[], stack<int> &Stack);
public:
	Graph(int V); // Constructor

	// function to add an edge to graph
	void addEdge(int v, int w);

	// prints a Topological Sort of the complete graph
	void topologicalSort();
};

Graph::Graph(int V)
{
	this->V = V;
	adj = new list<int>[V];
}

void Graph::addEdge(int v, int w)
{
	adj[v].push_back(w); // Add w to v’s list.
}

// A recursive function used by topologicalSort
void Graph::topologicalSortUtil(int v, bool visited[], stack<int> &Stack)
{
	// Mark the current node as visited.
	visited[v] = true;

	// Recur for all the vertices adjacent to this vertex
	list<int>::iterator i;
	for (i = adj[v].begin(); i != adj[v].end(); ++i)
		if (!visited[*i])
			topologicalSortUtil(*i, visited, Stack);

	// Push current vertex to stack which stores result
	Stack.push(v);
}

// The function to do Topological Sort. It uses recursive 
// topologicalSortUtil()
void Graph::topologicalSort()
{
	stack<int> Stack;

	// Mark all the vertices as not visited
	bool *visited = new bool[V];
	for (int i = 0; i < V; i++)
		visited[i] = false;

	// Call the recursive helper function to store Topological
	// Sort starting from all vertices one by one
	for (int i = 0; i < V; i++)
	if (visited[i] == false)
		topologicalSortUtil(i, visited, Stack);

	// Print contents of stack
	while (Stack.empty() == false)
	{
		cout << Stack.top() << " ";
		Stack.pop();
	}
}

// Driver program to test above functions
int main(int argc, char* argv[])
{
	// Create a graph given in the above diagram
	string seqlist[1000], line, buf;
	char str[1000];
	int spacerlist[1000][200];	
	int spacernum[1000];
	int total = 0;
	int noden = 0;
	int i, j, k, a;
	if(argc < 2) {
		cout<<"requires a file"<<endl;
		return 0;
	}
	ifstream file(argv[1]);
	total = 0;
	while(getline(file, line)) {
		//cout<<line<<endl;
		std::strcpy(str, line.c_str());
		a = 0;
		spacernum[total] = 0;
		for(int j = 1; j < line.length() - 3; j ++) {
			if(str[j - 1] == ' ') {
				a ++;
				if(a > 1) {
					sscanf(str + j, "%d", &k);
					spacerlist[total][spacernum[total] ++] = k;
					//printf("%s, array %d, spacer %d, total %d\n", str + j, i, k, spacernum[total]);
				}
			}
		}
		total ++;
	}
	file.close();
	noden = 0;
	for(i = 0; i < total; i ++) {
		for(j = 0; j < spacernum[i]; j ++) {
			if(spacerlist[i][j] > noden) noden = spacerlist[i][j];
		}
	}
	Graph g(noden);
	for(i = 0; i < total; i ++) {
		//cout<<"consider array "<<i<<" total node "<<spacernum[i]<<endl;
		for(j = 1; j < spacernum[i]; j ++) {
			//cout<<"add edge "<<spacerlist[i][j-1]-1<<" "<<spacerlist[i][j]-1<<endl;
			g.addEdge(spacerlist[i][j-1]-1, spacerlist[i][j]-1);
		}
	}

	//cout << "Following is a Topological Sort of the given graph \n";
	g.topologicalSort();

	cout<<endl;

	return 0;
}
