package sysinfo

import (
	"bufio"
	"bytes"
	"os"
	"os/exec"
	"runtime"
	"strings"
)

type SystemInfo struct {
	Hostname      string `json:"hostname"`
	OSName        string `json:"os_name"`
	OSVersion     string `json:"os_version"`
	Architecture  string `json:"architecture"`
	KernelVersion string `json:"kernel_version"`
}

func GetSystemInfo() (*SystemInfo, error) {
	info := &SystemInfo{
		Architecture: normalizeArchitecture(runtime.GOARCH),
	}

	hostname, err := os.Hostname()
	if err == nil {
		info.Hostname = hostname
	}

	info.OSName, info.OSVersion = detectOS()

	// Best effort kernel version
	out, err := exec.Command("uname", "-r").Output()
	if err == nil {
		info.KernelVersion = strings.TrimSpace(string(out))
	}

	return info, nil
}

func normalizeArchitecture(arch string) string {
	switch arch {
	case "amd64":
		return "x86_64"
	case "arm64":
		return "aarch64"
	default:
		return arch
	}
}

func detectOS() (name string, version string) {
	name = "unknown"
	version = "unknown"

	if data, err := os.ReadFile("/etc/os-release"); err == nil {
		name, version = parseOSRelease(data)
	} else if data, err := os.ReadFile("/etc/lsb-release"); err == nil {
		name, version = parseLSBRelease(data)
	}

	return name, version
}

func parseOSRelease(data []byte) (string, string) {
	var name, version string
	scanner := bufio.NewScanner(bytes.NewReader(data))
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if strings.HasPrefix(line, "ID=") {
			val := strings.TrimPrefix(line, "ID=")
			name = strings.Trim(strings.Trim(val, "\""), "'")
		} else if strings.HasPrefix(line, "VERSION_ID=") {
			val := strings.TrimPrefix(line, "VERSION_ID=")
			version = strings.Trim(strings.Trim(val, "\""), "'")
		}
	}
	return name, version
}

func parseLSBRelease(data []byte) (string, string) {
	var name, version string
	scanner := bufio.NewScanner(bytes.NewReader(data))
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if strings.HasPrefix(line, "DISTRIB_ID=") {
			name = strings.ToLower(strings.Trim(strings.TrimPrefix(line, "DISTRIB_ID="), "\""))
		} else if strings.HasPrefix(line, "DISTRIB_RELEASE=") {
			version = strings.Trim(strings.TrimPrefix(line, "DISTRIB_RELEASE="), "\"")
		}
	}
	return name, version
}
