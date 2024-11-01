{pkgs}: {
  deps = [
    pkgs.postgresql
    pkgs.openssl
    pkgs.python310Full
    pkgs.nodejs
    pkgs.git
    pkgs.curl
    pkgs.openssl
    pkgs.zlib
    pkgs.libffi
    pkgs.sqlite
    pkgs.gcc
    pkgs.gdbm
    pkgs.libnsl
  ];
}
