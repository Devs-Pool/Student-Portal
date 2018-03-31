#include <bits/stdc++.h> 
using namespace std;

const int N = 500005

int tin[N], tout[N], level[N], mag[N], mp[N], color[N], freq[N];
int timer, n, block, q;
vector <int> g[N];

struct node{
	int l, r, k, ans, idx;
}query[N];

void dfs(int v, int p){
	tin[v] = ++timer;
	mp[timer] = v;
	for(auto it : g[v]){
		if(it != p){
			level[it] = level[v] + 1;
			dfs(it, v);
		}
	}
	tout[v] = timer;
}

bool cmp(node a, node b){
	if(a.l/block != b.l/block)
		return a.l/block < b.l/block;
	else
		return a.r < b.r;
}
bool cmp1(node a, node b){
	return a.idx < b.idx;
}
void add(int i){
	freq[++color[mag[i]]]++;
}

void remove(int i){
	freq[color[mag[i]]--]--;
}

int main(){
	scanf("%d %d", &n, &q);
	block = sqrt(n);
	for(int i = 1; i <= n; ++i){
		scanf("%d", mag+i);
	}
	for(int i = 1; i <n; ++i){
		int x, y;
		scanf("%d %d", &x,  &y);
		g[x].push_back(y);
		g[y].push_back(x);
	}
	dfs(1,0);
	for(int i = 0; i < q; ++i){
		int x;
		scanf("%d %d", &x, &query[i].k);
		query[i].l = tin[x];
		query[i].r = tout[x];
		query[i].idx = i;
		query[i].ans = freq[query[0].k];
	}

	sort(query, query+q,cmp);
	int curl = query[0].l, curr = query[0].r;
	
	for(int i = curl; i<= curr; ++i){
		add(mp[i]);
	}
	query[0].ans = freq[query[0].k];
	for(int i = 1; i < q; ++i){
		while(curl < query[i].l){
			remove(mp[curl++]);
		}
		while(curr < query[i].r){
			add(mp[++curr]);
		}
		while(curl > query[i].l){
			add(mp[--curl]);
		}
		while(curr > query[i].r){
			remove(mp[curr--]);
		}
		query[i].ans = freq[query[i].k];
	}
	sort(query, query+q, cmp1);
	for(int i = 0; i < q; ++i){
		printf("%d\n", query[i].ans);
	}
}