FROM ros:foxy

RUN apt-get -y update \
    && apt-get -y install --no-install-recommends python3-pip



# ** [Optional] Uncomment this section to install additional packages. **
# . /opt/ros/$ROS_DISTRO/setup.sh \
#    && add-apt-repository universe \
# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt-get -y update \
#    && apt-get -y install --no-install-recommends python3-pip \
    #
    # Clean up
    #&& apt-get autoremove -y \
    #&& apt-get clean -y \
    #&& rm -rf /var/lib/apt/lists/*
# ENV DEBIAN_FRONTEND=dialog
# Set up auto-source of workspace for ros user