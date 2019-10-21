PROTOGEN = gogofaster

PROTOC = protoc --$(PROTOGEN)_out=. *.proto -I.:$(shell go env GOPATH)/src --proto_path=$(shell go env GOPATH)/src/github.com/gogo/protobuf/protobuf

PROTOCOL_PROTOS = $(wildcard proto/*.proto)
PROTOCOL_GOPROTOS = $(PROTOCOL_PROTOS:.proto=.pb.go)

INDEXER_PROTOS = $(wildcard service/indexer/model/protocol/*.proto)
INDEXER_GOPROTOS = $(INDEXER_PROTOS:.proto=.pb.go)

PAYMENT_PROXY_PROTOS = $(wildcard service/paymentproxy/model/entity/*.proto)
PAYMENT_PROXY_GOPROTOS = $(PAYMENT_PROXY_PROTOS:.proto=.pb.go)

#COMMIT_ID=`/usr/bin/git log --oneline -n 1 | /usr/bin/cut -d " " -f1`
COMMIT_ID=$(shell git log --oneline -n 1 | cut -d " " -f1)
GIT_BRANCH_NAME = $(shell git rev-parse --abbrev-ref HEAD)
GIT_COMMIT_COUNT = $(shell git rev-list --count $(GIT_BRANCH_NAME))
GO_LD_FLGAS = "-X main._BUILDVERSION_='$(COMMIT_ID)' -X github.com/PPIO/go-ppio/service.BUILD_NUMBER=$(GIT_COMMIT_COUNT) -X github.com/PPIO/go-ppio/service.BUILD_BRANCH_NAME=$(GIT_BRANCH_NAME) -X github.com/PPIO/go-ppio/service.BUILD_COMMIT_ID=$(COMMIT_ID)"


.PHONY: clean all

all: center bootstrap indexer verifier gateway ppio poss miner copyall

clean:
	go clean
	rm proto/*.pb.go
	rm service/indexer/model/protocol/*.pb.go
	rm $(PAYMENT_PROXY_GOPROTOS)

$(PROTOCOL_GOPROTOS): $(PROTOCOL_PROTOS)
	cd proto; $(PROTOC)

$(INDEXER_GOPROTOS): $(INDEXER_PROTOS)
	cd service/indexer/model/protocol; $(PROTOC) -I.:$(shell go env GOPATH)/src

$(PAYMENT_PROXY_GOPROTOS): $(PAYMENT_PROXY_PROTOS)
	cd service/paymentproxy/model/entity; $(PROTOC)

buildprotos: $(PROTOCOL_GOPROTOS) $(INDEXER_GOPROTOS) $(PAYMENT_PROXY_GOPROTOS)

.PHONY: buildprotos android

.PHONY: test test_ppio test_miner test_miner_storage test_peer_job test_peer

test: test_peer

test_peer: test_peer_job

test_peer_job: buildprotos
	cd service/peer/job; go test

android: buildprotos
	cd sdk/poss; gomobile bind -target=android -v

center: buildprotos
	cd cmd/center;    go build -ldflags "-X main._BUILDVERSION_='$(COMMIT_ID)'"

bootstrap: buildprotos
	cd cmd/bootstrap; go build -ldflags "-X main._BUILDVERSION_='$(COMMIT_ID)'"

indexer: buildprotos 
	cd cmd/indexer;   go build -ldflags "-X main._BUILDVERSION_='$(COMMIT_ID)'"

verifier: buildprotos
	cd cmd/verifier;  go build -ldflags "-X main._BUILDVERSION_='$(COMMIT_ID)'"

gateway: buildprotos
	cd cmd/gateway;   go build -ldflags "-X main._BUILDVERSION_='$(COMMIT_ID)'"
	
ppio: buildprotos
	cd cmd/ppio;      go build -ldflags "-X main._BUILDVERSION_='$(COMMIT_ID)'"
	
poss: buildprotos
	cd cmd/poss;      go build -ldflags $(GO_LD_FLGAS)

miner: buildprotos
	cd cmd/miner;     go build -ldflags "-X main._BUILDVERSION_='$(COMMIT_ID)'"

goenfi: buildprotos
	cd cmd/goenfi;    go build -ldflags "-X main._BUILDVERSION_='$(COMMIT_ID)'"

paymentproxy: buildprotos $(PAYMENT_PROXY_GOPROTOS)
	cd cmd/paymentproxy; go build

cpool_demo: buildprotos
	cd cmd/cpool_demo;   go build

settlement: buildprotos
	cd cmd/settlement;   go build

copyall:
	mkdir -p ./bin/$(COMMIT_ID)
	cp cmd/center/center         ./bin/$(COMMIT_ID)/center
	cp cmd/bootstrap/bootstrap   ./bin/$(COMMIT_ID)/bootstrap
	cp cmd/indexer/indexer       ./bin/$(COMMIT_ID)/indexer
	cp cmd/indexer/indexer.json  ./bin/$(COMMIT_ID)/indexer.json
	cp cmd/verifier/verifier     ./bin/$(COMMIT_ID)/verifier
	cp cmd/gateway/gateway       ./bin/$(COMMIT_ID)/gateway
	cp cmd/ppio/ppio             ./bin/$(COMMIT_ID)/ppio
	cp cmd/poss/poss             ./bin/$(COMMIT_ID)/poss
	cp cmd/miner/miner           ./bin/$(COMMIT_ID)/miner

	cd ./bin; ln -sf ./$(COMMIT_ID)/center       center
	cd ./bin; ln -sf ./$(COMMIT_ID)/bootstrap    bootstrap
	cd ./bin; ln -sf ./$(COMMIT_ID)/indexer.json indexer.json
	cd ./bin; ln -sf ./$(COMMIT_ID)/indexer      indexer
	cd ./bin; ln -sf ./$(COMMIT_ID)/verifier     verifier
	cd ./bin; ln -sf ./$(COMMIT_ID)/gateway      gateway
	cd ./bin; ln -sf ./$(COMMIT_ID)/ppio         ppio
	cd ./bin; ln -sf ./$(COMMIT_ID)/poss         poss
	cd ./bin; ln -sf ./$(COMMIT_ID)/miner        miner




