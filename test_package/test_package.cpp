#include <iostream>
#include <cpuinfo.h>

int main()
{
	cpuinfo_initialize();
    std::cout << "Bincrafters on " << cpuinfo_get_cores() " cores\n";
    cpuinfo_deinitialize();
}
