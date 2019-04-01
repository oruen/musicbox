package main

import (
	"fmt"
	"github.com/Tinkerforge/go-api-bindings/ipconnection"
	"github.com/Tinkerforge/go-api-bindings/nfc_bricklet"
)

const ADDR string = "localhost:4223"
const UID string = "unT" // Change XYZ to the UID of your NFC Bricklet.

func fatal_err(err error) {
	panic(err)
}

func main() {
	ipcon := ipconnection.New()
	defer ipcon.Close()
	nfc, err := nfc_bricklet.New(UID, &ipcon) // Create device object.
	if err != nil {
		fatal_err(err)
	}

	iperr := ipcon.Connect(ADDR) // Connect to brickd.
	if iperr != nil {
		panic(iperr)
	}
	defer ipcon.Disconnect()
	// Don't use device before ipcon is connected.

	reg_status := nfc.RegisterReaderStateChangedCallback(func(state nfc_bricklet.ReaderState, idle bool) {
		if state == nfc_bricklet.ReaderStateRequestTagIDReady {
			tagID, tagType, err := nfc.ReaderGetTagID()
			if err != nil {
				fatal_err(err)
			}
			fmt.Printf("Found tag of type %d with ID %v", tagType, tagID)
		} else if state == nfc_bricklet.ReaderStateRequestTagIDError {
			fmt.Println("Request tag ID error")
		}
		if idle {
			nfc.ReaderRequestTagID()
		}
	})

	fmt.Printf("Callback register status %d\n", reg_status)

	// Enable reader mode
	mode_err := nfc.SetMode(nfc_bricklet.ModeReader)
	if mode_err != nil {
		fatal_err(err)
	}

	fmt.Print("Press enter to exit.")
	fmt.Scanln()
}
