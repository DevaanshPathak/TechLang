# Package initialization file for myutils
# This file is executed when you do: import myutils

# Define package-level variables
set myutils_version 100

# Define a package-level function
def get_version
    print myutils_version
end
export get_version

# Re-export commonly used functions from submodules
# (users can access these directly from myutils)
