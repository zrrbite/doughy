from doughy.controller import BangBangController, HeaterAction


class TestBangBangController:
    def test_heater_turns_on_below_deadband(self):
        c = BangBangController(target_temp=26.0, deadband=0.5)
        assert c.decide(25.4) == HeaterAction.ON

    def test_heater_turns_off_above_deadband(self):
        c = BangBangController(target_temp=26.0, deadband=0.5)
        c.decide(25.0)  # turn on first
        assert c.decide(26.6) == HeaterAction.OFF

    def test_no_change_within_deadband(self):
        c = BangBangController(target_temp=26.0, deadband=0.5)
        c.decide(25.0)  # turn on
        assert c.decide(25.8) == HeaterAction.NO_CHANGE

    def test_no_change_when_already_on_and_still_cold(self):
        c = BangBangController(target_temp=26.0, deadband=0.5)
        c.decide(25.0)  # turn on
        assert c.decide(25.2) == HeaterAction.NO_CHANGE

    def test_no_change_when_already_off_and_still_warm(self):
        c = BangBangController(target_temp=26.0, deadband=0.5)
        assert c.decide(27.0) == HeaterAction.NO_CHANGE

    def test_update_target(self):
        c = BangBangController(target_temp=26.0, deadband=0.5)
        c.update_target(30.0)
        # Now 26°C is below the new deadband (29.5), so heater should turn on
        assert c.decide(26.0) == HeaterAction.ON

    def test_exact_boundary_low_no_change(self):
        c = BangBangController(target_temp=26.0, deadband=0.5)
        # At exactly target - deadband (25.5), should NOT turn on
        assert c.decide(25.5) == HeaterAction.NO_CHANGE

    def test_exact_boundary_high_no_change(self):
        c = BangBangController(target_temp=26.0, deadband=0.5)
        c.decide(25.0)  # turn on
        # At exactly target + deadband (26.5), should NOT turn off
        assert c.decide(26.5) == HeaterAction.NO_CHANGE

    def test_full_cycle(self):
        c = BangBangController(target_temp=26.0, deadband=0.5)
        # Start cold -> heater on
        assert c.decide(24.0) == HeaterAction.ON
        # Warming up, still in band -> no change
        assert c.decide(25.8) == HeaterAction.NO_CHANGE
        assert c.decide(26.0) == HeaterAction.NO_CHANGE
        assert c.decide(26.4) == HeaterAction.NO_CHANGE
        # Overshot -> heater off
        assert c.decide(26.6) == HeaterAction.OFF
        # Cooling down, still in band -> no change
        assert c.decide(26.2) == HeaterAction.NO_CHANGE
        assert c.decide(25.8) == HeaterAction.NO_CHANGE
        # Dropped below -> heater on again
        assert c.decide(25.4) == HeaterAction.ON
