#include "plugin.hpp"

#include <algorithm>
#include <numeric>
#include <thread>

namespace plugin {

std::string describe(Mode m) {
  return m == Mode::Fast ? "fast (approximate)" : "accurate (slow)";
}

double Filter::apply_all(const std::vector<double>& xs) const {
  double total = 0.0;
  for (double x : xs) {
    total += apply(x);  // virtual dispatch -> may re-enter Python
  }
  return total;
}

std::unique_ptr<Filter> make_scale(double factor) {
  return std::make_unique<Scale>(factor);
}

double pipeline_sum(const Filter& f, const std::vector<double>& xs) {
  return f.apply_all(xs);
}

double transform_sum(const std::vector<double>& xs,
                     const std::function<double(double)>& fn) {
  double total = 0.0;
  for (double x : xs) {
    total += fn(x);
  }
  return total;
}

void Button::click() {
  ++clicks_;
  if (cb_) {
    cb_(clicks_);
  }
}

std::vector<double> parallel_apply(const std::vector<double>& xs,
                                   const std::function<double(double)>& fn,
                                   std::size_t n_threads) {
  std::vector<double> out(xs.size());
  n_threads = std::max<std::size_t>(1, std::min(n_threads, xs.size()));

  std::vector<std::thread> pool;
  for (std::size_t t = 0; t < n_threads; ++t) {
    pool.emplace_back([&, t] {
      for (std::size_t i = t; i < xs.size(); i += n_threads) {
        out[i] = fn(xs[i]);  // calls into Python from a non-main thread
      }
    });
  }
  for (auto& th : pool) {
    th.join();
  }
  return out;
}

}  // namespace plugin
