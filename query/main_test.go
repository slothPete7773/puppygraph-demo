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

	// Get all the nodes (vertices) in the Graph.
	query := `
  MATCH (n:customer)-[r:creates]->(m:transaction) 
  WHERE m.payment_method = 'debit_card' and m.status = 'failed'
  RETURN 
    n.customer_id,
    n.email,
    n.loyalty_tier,
    m.amount,
    m.currency
  LIMIT 100
  `
	fmt.Println("All nodes (vertices) in the graph:")
	results, err := session.Run(query, nil)
	if err != nil {
		fmt.Println("Error executing query:", err)
		return
	}

	i := 0
	for results.Next() {
		fmt.Println(results.Record().Values)

		i += 1
		if i == 100 {
			break
		}
	}
	if err = results.Err(); err != nil {
		fmt.Println("Error with query results:", err)
	}
}
