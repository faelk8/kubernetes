package main

import (
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/", Hello)
	fmt.Println("Servidor Go executando na porta 8000...")
	http.ListenAndServe(":8000", nil)
}

func Hello(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "<h1>Rafael Batista</h1>")
}
