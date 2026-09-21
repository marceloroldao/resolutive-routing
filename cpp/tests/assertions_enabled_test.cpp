#ifdef NDEBUG
#error "resolutive-routing test targets must keep assertions enabled in Release builds"
#endif

#include <cassert>

int main() {
    bool evaluated = false;
    assert((evaluated = true));
    return evaluated ? 0 : 1;
}
