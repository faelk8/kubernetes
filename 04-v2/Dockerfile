FROM golang:latest

WORKDIR /app
COPY . .

RUN go build -o server .

CMD ["./server"]