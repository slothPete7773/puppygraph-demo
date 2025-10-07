package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/neo4j/neo4j-go-driver/v4/neo4j"
)

func main() {
	// Creating the connection to the PuppyGraph.
	query := `
    USING enableCypherEngineProperties 'true'
    MATCH (c:customer)-[r:creates]->(t:transaction)
    WHERE t.payment_method = 'debit_card' and t.status = 'failed'
    RETURN
      c, r, t
    ORDER BY t.transaction_id
    LIMIT 10
    `

	data, err := QueryGraph(query)
	if err != nil {
		log.Fatal(err.Error())
	}

	err = ExportToJson(data)
	if err != nil {
		log.Fatal(err.Error())
	}

	log.Println("Done")
}

func QueryGraph(queryStmt string) (GraphData, error) {

	uri := "bolt://localhost:7687"
	username := "admin"
	password := "admin"
	driver, err := neo4j.NewDriver(uri, neo4j.BasicAuth(username, password, ""))
	if err != nil {
		fmt.Println("Error creating driver:", err)
		panic(err)
	}
	defer driver.Close()

	// Open a new session using the driver
	sessionConfig := neo4j.SessionConfig{AccessMode: neo4j.AccessModeRead}
	session := driver.NewSession(sessionConfig)
	defer session.Close()

	response := GraphData{
		Nodes: []neo4j.Node{},
		Edges: []neo4j.Relationship{},
	}

	fmt.Println("All nodes (vertices) in the graph:")
	results, err := session.Run(queryStmt, nil)
	if err != nil {
		return GraphData{}, fmt.Errorf("Error executing query: %w", err)
	}

	for results.Next() {
		record := results.Record()
		if node, ok := record.Get("c"); ok {
			response.Nodes = append(response.Nodes, node.(neo4j.Node))
		}
		if node, ok := record.Get("t"); ok {
			response.Nodes = append(response.Nodes, node.(neo4j.Node))
		}

		if rel, ok := record.Get("r"); ok {
			response.Edges = append(response.Edges, rel.(neo4j.Relationship))
		}

	}
	if err = results.Err(); err != nil {
		fmt.Println("Error with query results:", err)
	}

	return response, nil
}

func ExportToJson(data GraphData) error {
	f, err := os.Create("graph-data.json")
	if err != nil {
		return fmt.Errorf("error-create-file: %w", err)
	}

	enc := json.NewEncoder(f)
	enc.Encode(data)

	return nil
}
