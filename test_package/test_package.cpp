#include <iostream>
extern "C" {
#include <cpuinfo.h>
}

int main()
{
	cpuinfo_initialize();
    std::cout << "Bincrafters on " << cpuinfo_get_processors_count() << " cores\n";
    cpuinfo_deinitialize();
}
