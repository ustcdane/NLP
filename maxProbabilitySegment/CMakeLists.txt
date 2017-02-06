cmake_minimum_required(VERSION 3.1.0)

project(maxProbabilitySegment)

message("${CMAKE_BUILD_TYPE}")
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
message(STATUS "C++11 support has been enabled by default.")

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

#add_subdirectory("../pinyinannotation/SegmentorForPyAnno" "SegmentorForPyAnno")
#add_subdirectory(pugixml)

# base options
#set(USE_LIBXML ON CACHE BOOL "" FORCE)

#include_directories(
#	"${PROJECT_SOURCE_DIR}"
#	"${PROJECT_SOURCE_DIR}/src"
#	)
	
set(FOLDERS src)

foreach (folder IN LISTS FOLDERS)
	# add cpp/h 
	FILE(GLOB_RECURSE SRC "${PROJECT_SOURCE_DIR}/${folder}/*.cpp" "${PROJECT_SOURCE_DIR}/${folder}/*.h")
	# remove *main.cpp
	#FILE(GLOB_RECURSE M "${PROJECT_SOURCE_DIR}/${folder}/*_main.cpp")
	
	#if (M)
	#	LIST(REMOVE_ITEM SRC ${M})
	#endif()
	
	LIST(APPEND CC_FILES ${SRC})
	source_group(${folder} FILES ${SRC})
endforeach(folder)

add_executable(${PROJECT_NAME} ${CC_FILES})
