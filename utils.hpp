#include <string>
#include <vector>
#include <utility>
#include <iterator>
#include <sstream>

namespace mine {
	using uint = unsigned int;
	
    template <typename N>
    class countup_itr {
        N i;
    public:
        countup_itr() : i(0) {}
        countup_itr(N i) : i(i) {}
        
        N operator*() { return i; }
        countup_itr& operator++() { ++i; return *this; }
        bool operator!=(const countup_itr& v) { return i != v.i; }
    };

    template <typename N = int>
    class irange {
	    N start, stop;
    public:
        irange(N start, N end) : start(start), stop(stop) {}
        irange(N end) : start(0), stop(end) {}
        auto begin() { return countup_itr<N>(start); }
        auto end()   { return countup_itr<N>(stop); }
    };
    
    
    template <typename N, typename I>
    class container_itr {
        N i;
        I it;
    public:
        container_itr(N i, I it) : i(i), it(it) {}
        
        auto operator*() { return std::make_pair(i, *it); }
        container_itr& operator++() { it++; i++; return *this; }
        bool operator!=(const container_itr& v) { return it != v.it && i != v.i; }
    };
    
    template<typename I, typename N = int>
    class index_base {
        I ib, ie;
    public:
        index_base(I ib, I ie) : ib(ib), ie(ie) {}
        auto begin() { return container_itr<N, I>(0, ib); }
        auto end()   { return container_itr<N, I>(std::distance(ib, ie), ie); }
    };
    
    template<typename N = int, typename C>
    auto index(C container) {
        return index_base<decltype(std::begin(container)), N>(std::begin(container), std::end(container));
    }
    
    
    unsigned int stoui(const std::string& str) {
        std::istringstream iss(str);
        unsigned int out = 0;
        iss >> out;
        return out;
    }
}
