cmake_minimum_required(VERSION 3.8)
project(robo_nav2)

# Opciones de compilación
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Dependencias
find_package(ament_cmake REQUIRED)
find_package(nav2_bringup REQUIRED)
find_package(nav2_common REQUIRED)

# 🔹 Forzar detección de cambios en carpetas (importante)
file(GLOB_RECURSE RESOURCE_FILES
  "${CMAKE_CURRENT_SOURCE_DIR}/launch/*"
  "${CMAKE_CURRENT_SOURCE_DIR}/config/*"
  "${CMAKE_CURRENT_SOURCE_DIR}/maps/*"
  "${CMAKE_CURRENT_SOURCE_DIR}/rviz/*"
)

# 🔹 Instalación de recursos
install(DIRECTORY
  launch
  config
  maps
  rviz
  DESTINATION share/${PROJECT_NAME}
)

# Testing opcional
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()