import ntcore
import time
if __name__ == "__main__":
    inst = ntcore.NetworkTableInstance.getDefault()
    table = inst.getTable("SmartDashboard")
    xSub = table.getDoubleTopic("x").getEntry(1)
    ySub = table.getDoubleTopic("y").getEntry(0)

    inst.addConnectionListener(True, lambda a : print(a))
    inst.setServer
    # start a NT4 client
    inst.startClient4("example client")

    # connect to a roboRIO with team number TEAM
    inst.setServerTeam(2898)

    # starting a DS client will try to get the roboRIO address from the DS application
    #inst.startDSClient()

    # connect to a specific host/port
    #inst.setServer("host", ntcore.NetworkTableInstance.kDefaultPort4)
    print( inst.isConnected())


    while True:
        print( inst.isConnected())

        time.sleep(1)
        x = xSub.get()
        xSub.set(2)
        y = ySub.get()
        print(f"X: {x} Y: {y}")