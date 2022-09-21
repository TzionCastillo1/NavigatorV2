FROM ros:foxy

RUN apt-get -y update \
    && apt-get -y install --no-install-recommends python3-pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN echo ". /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc

#RUN . /opt/ros/$ROS_DISTRO/setup.bash
#RUN colcon build
#RUN . install/setup.bash
#RUN ros2 launch launch/navigator_launch.py



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