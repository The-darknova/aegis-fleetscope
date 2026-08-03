package sysinfo

import (
	"testing"
)

func TestParseOSRelease(t *testing.T) {
	mockData := []byte(`PRETTY_NAME="Ubuntu 22.04 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
`)

	name, version := parseOSRelease(mockData)
	if name != "ubuntu" {
		t.Errorf("Expected OS name 'ubuntu', got '%s'", name)
	}
	if version != "22.04" {
		t.Errorf("Expected OS version '22.04', got '%s'", version)
	}
}

func TestParseOSReleaseRHEL(t *testing.T) {
	mockData := []byte(`NAME="Red Hat Enterprise Linux"
VERSION="9.2 (Plow)"
ID="rhel"
ID_LIKE="fedora"
VERSION_ID='9.2'
PLATFORM_ID="platform:el9"
PRETTY_NAME="Red Hat Enterprise Linux 9.2 (Plow)"
ANSI_COLOR="0;31"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:redhat:enterprise_linux:9::baseos"
HOME_URL="https://www.redhat.com/"
DOCUMENTATION_URL="https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9"
BUG_REPORT_URL="https://bugzilla.redhat.com/"
`)

	name, version := parseOSRelease(mockData)
	if name != "rhel" {
		t.Errorf("Expected OS name 'rhel', got '%s'", name)
	}
	if version != "9.2" {
		t.Errorf("Expected OS version '9.2', got '%s'", version)
	}
}

func TestParseLSBRelease(t *testing.T) {
	mockData := []byte(`DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=20.04
DISTRIB_CODENAME=focal
DISTRIB_DESCRIPTION="Ubuntu 20.04 LTS"
`)

	name, version := parseLSBRelease(mockData)
	if name != "ubuntu" {
		t.Errorf("Expected OS name 'ubuntu', got '%s'", name)
	}
	if version != "20.04" {
		t.Errorf("Expected OS version '20.04', got '%s'", version)
	}
}

func TestNormalizeArchitecture(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"amd64", "x86_64"},
		{"arm64", "aarch64"},
		{"386", "386"},
	}

	for _, test := range tests {
		result := normalizeArchitecture(test.input)
		if result != test.expected {
			t.Errorf("For arch %s, expected %s but got %s", test.input, test.expected, result)
		}
	}
}
