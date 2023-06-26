#!/bin/bash
#Installation

is_installed_python_smbus=False
is_installed_python_opencv=False

if [ "$(whoami)" != "root" ] ; then
    echo -e "You must run this script as root."
    exit
fi

sudo apt-get update

function if_continue(){
    while :; do
        echo  -e "(yes/no) \c"
        read input_item
        if [ $input_item = "yes" ]; then
            break
        elif [ $input_item = "no" ]; then
            return 0
        else
            echo -e "Input error, please try again."
        fi
    done
    return 1
}

function end(){
    print_result
    echo -e "Exiting..."
    exit
}

function print_result(){
    echo -e "Installation result:"
    echo -e "python-smbus  \c"
    if $is_installed_python_smbus; then
        echo -e "Success"
    else
        echo -e "Failed"
    fi
    echo -e "python-opencv  \c"
    if $is_installed_python_opencv; then
        echo -e "Success"
    else
        echo -e "Failed"
    fi
}

###################################
# install python-pip python-smbus python-opencv runtime #
###################################

echo -e "\nInstalling python3-smbus and git\n"
if sudo apt-get install python3-smbus git -y; then
    echo -e "    Successfully installed python-smbus and git\n"
    is_installed_python_smbus=true
else
    echo -e "    Failed to installed python-smbus and git\n"
    echo -e "    Do you want to skip this? \c"
    if_continue
    if [ $? = 1 ] ; then
        echo -e "    Skipped python-smbus and git installation."
    else
        end
    fi
fi

echo -e "\nInstalling python3-opencv \n"
if sudo apt-get install python3-opencv -y; then
    echo -e "    Successfully installed python-opencv \n"
    is_installed_python_opencv=true
else
    echo -e "    Failed to installed python-opencv \n"
    echo -e "    Do you want to skip this? \c"
    if_continue
    if [ $? = 1 ] ; then
        echo -e "    Skipped python-opencv installation."
    else
        end
    fi
fi

print_result

echo -e "The stuff you have change may need reboot to take effect."
echo -e "Do you want to reboot immediately? \c"
if_continue
if [ $? = 1 ]; then
    echo -e "Rebooting..."
    sudo reboot
else
    echo -e "Exiting..."
    exit
fi
