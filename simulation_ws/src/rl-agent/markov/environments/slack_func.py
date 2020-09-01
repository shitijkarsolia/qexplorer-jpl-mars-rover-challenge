
    def rover_reset(self):
        # Reset Rover-related Episodic variables
        rospy.wait_for_service('gazebo/set_model_state')
        self.x = INITIAL_POS_X
        self.y = INITIAL_POS_Y
        # Put the Rover at the initial position
        model_state = ModelState()
        model_state.pose.position.x = INITIAL_POS_X
        model_state.pose.position.y = INITIAL_POS_Y
        model_state.pose.position.z = INITIAL_POS_Z
        model_state.pose.orientation.x = INITIAL_ORIENT_X
        model_state.pose.orientation.y = INITIAL_ORIENT_Y
        model_state.pose.orientation.z = INITIAL_ORIENT_Z
        model_state.pose.orientation.w = INITIAL_ORIENT_W
        model_state.twist.linear.x = 0
        model_state.twist.linear.y = 0
        model_state.twist.linear.z = 0
        model_state.twist.angular.x = 0
        model_state.twist.angular.y = 0
        model_state.twist.angular.z = 0
        model_state.model_name = 'rover'
        # List of joints to reset (this is all of them)
        joint_names_list = ["rocker_left_corner_lb",
                            "rocker_right_corner_rb",
                            "body_rocker_left",
                            "body_rocker_right",
                            "rocker_right_bogie_right",
                            "rocker_left_bogie_left",
                            "bogie_left_corner_lf",
                            "bogie_right_corner_rf",
                            "corner_lf_wheel_lf",
                            "imu_wheel_lf_joint",
                            "bogie_left_wheel_lm",
                            "imu_wheel_lm_joint",
                            "corner_lb_wheel_lb",
                            "imu_wheel_lb_joint",
                            "corner_rf_wheel_rf",
                            "imu_wheel_rf_joint",
                            "bogie_right_wheel_rm",
                            "imu_wheel_rm_joint",
                            "corner_rb_wheel_rb",
                            "imu_wheel_rb_joint"]
        # Angle to reset joints to
        joint_positions_list = [0.0 for _ in range(len(joint_names_list))]
        #self.gazebo_model_state_service(model_state)
        self.gazebo_model_configuration_service(model_name='rover', urdf_param_name='rover_description', joint_names=joint_names_list, joint_positions=joint_positions_list)
        self.reset_models()
        self.last_collision_threshold = sys.maxsize
        self.last_position_x = self.x
        self.last_position_y = self.y
        time.sleep(SLEEP_AFTER_RESET_TIME_IN_SECOND)
        self.distance_travelled = 0
        self.current_distance_to_checkpoint = INITIAL_DISTANCE_TO_CHECKPOINT
        self.steps = 0
        self.reward_in_episode = 0
        self.collision = False
        self.closer_to_checkpoint = False
        self.power_supply_range = MAX_STEPS
        self.reached_waypoint_1 = False
        self.reached_waypoint_2 = False
        self.reached_waypoint_3 = False
        self.max_lin_accel_x = 0
        self.max_lin_accel_y = 0
        self.max_lin_accel_z = 0
        # First clear the queue so that we set the state to the start image
        _ = self.image_queue.get(block=True, timeout=None)
        self.set_next_state()