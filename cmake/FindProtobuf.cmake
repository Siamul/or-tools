@@ -24,3 +24,9 @@ find_package(PkgConfig REQUIRED)

pkg_check_modules(PROTOBUF REQUIRED protobuf IMPORTED_TARGET GLOBAL)
add_library(protobuf::libprotobuf ALIAS PkgConfig::PROTOBUF)

find_program(PROTOC_EXEC protoc REQUIRED)
add_executable(protobuf::protoc IMPORTED GLOBAL)
set_target_properties(protobuf::protoc PROPERTIES
  IMPORTED_LOCATION ${PROTOC_EXEC}
)