package main

import (
	"fmt"
	"testing"

	"github.com/neo4j/neo4j-go-driver/v4/neo4j"
)

func TestMain(t *testing.T) {
	// Creating the connection to the PuppyGraph.
	uri := "bolt://localhost:7687"
	username := "admin"
	password := "admin"
	driver, err := neo4j.NewDriver(uri, neo4j.BasicAuth(username, password, ""))
	if err != nil {
		fmt.Println("Error creating driver:", err)
		return
	}
	defer driver.Close()

	// Open a new session using the driver
	sessionConfig := neo4j.SessionConfig{AccessMode: neo4j.AccessModeRead}
	session := driver.NewSession(sessionConfig)
	defer session.Close()

	query := `
  USING enableCypherEngineProperties 'true'
  MATCH (c:customer)-[r:creates]->(t:transaction) 
  WHERE t.payment_method = 'debit_card' and t.status = 'failed'
  RETURN 
    c, r, t
  ORDER BY t.transaction_id
  LIMIT 10
  `
	fmt.Println("All nodes (vertices) in the graph:")
	results, err := session.Run(query, nil)
	if err != nil {
		fmt.Println("Error executing query:", err)
		return
	}

	i := 0
	for results.Next() {
		record := results.Record()

		if node, ok := record.Get("c"); ok {

			n := node.(neo4j.Node)
			fmt.Printf("Node n:\n")
			fmt.Printf("  ID: %d\n", n.Id)
			fmt.Printf("  Labels: %v\n", n.Labels)
			fmt.Printf("  Props: %v\n", n.Props)

			_id := n.Props["_id"]
			fmt.Printf("_id: %v\n", _id)
		}

		if node, ok := record.Get("t"); ok {
			n := node.(neo4j.Node)
			fmt.Printf("Node n:\n")
			fmt.Printf("  ID: %d\n", n.Id)
			fmt.Printf("  Labels: %v\n", n.Labels)
			fmt.Printf("  Props: %v\n", n.Props)

			_id := n.Props["_id"]
			fmt.Printf("_id: %v\n", _id)
		}

		if rel, ok := record.Get("r"); ok {
			r := rel.(neo4j.Relationship)
			fmt.Printf("Relationship r:\n")
			fmt.Printf("  ID: %d\n", r.Id)
			fmt.Printf("  Type: %s\n", r.Type)
			fmt.Printf("  StartId: %d\n", r.StartId)
			fmt.Printf("  EndId: %d\n", r.EndId)
			fmt.Printf("  Props: %v\n", r.Props)
		}

		i += 1
		if i == 1 {
			break
		}
	}
	if err = results.Err(); err != nil {
		fmt.Println("Error with query results:", err)
	}
}
