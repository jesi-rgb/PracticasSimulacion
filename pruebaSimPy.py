import simpy

def main():
    env = simpy.Environment()
    env.process(traffic_l(env))
    env.run(until=1220)
    print("Finished")

def traffic_l(env):
    while True:
        print("Yellow at "+str(env.now))
        yield env.timeout(30)
        print("Blue at "+str(env.now))
        yield env.timeout(4)
        print("Red at "+str(env.now))
        yield env.timeout(10)

if __name__ == '__main__':
    main()
