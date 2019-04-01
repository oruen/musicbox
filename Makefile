build:
	env GOOS=linux GOARCH=arm GOARM=7 go build

clean:
	rm musicbox

release:
	goreleaser release --skip-validate --rm-dist
