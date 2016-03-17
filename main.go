package main

import (
	"compress/gzip"
	"encoding/json"
	"fmt"
	"os"
	
	"github.com/fluhus/gostuff/nlp/wordnet"
)

// Modify this path to your local WordNet root.
const input = "../wordnet/dict"

func main() {
	fmt.Println("Parsing database...")
	wn, err := wordnet.Parse(input)
	checkError(err)
	
	fmt.Println("Encoding in JSON...")
	j, err := json.MarshalIndent(wn, "", "  ")
	checkError(err)
	
	fmt.Println("Writing output...")
	f, err := os.Create("wordnet.json.gz")
	checkError(err)
	z := gzip.NewWriter(f)
	_, err = z.Write(j)
	checkError(err)
	z.Close()
	f.Close()
	
	fmt.Println("Done!")
}

func checkError(err error) {
	if err != nil {
		fmt.Println("ERROR:", err)
		os.Exit(2)
	}
}

