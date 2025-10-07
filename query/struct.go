package main

import "github.com/neo4j/neo4j-go-driver/v4/neo4j"

type GraphData struct {
	Nodes []neo4j.Node
	Edges []neo4j.Relationship
}
