#include <bits/stdc++.h>
using namespace std;
#define ll long long
typedef struct node{
	ll left;
	ll right;
	ll answer;
	ll len;
	node(){
		left=right=answer=len=0;
	}
}node;
node seg[500005];
string s;
ll ans=0;
void build(ll node,ll st,ll en){
	if(st == en){
		seg[node].len=1;
		if(s[st-1]=='a')
			seg[node].left=1;
		else
			seg[node].right=1;
		return;
	}
	ll mid = (st+en)/2;
	build(2*node,st,mid);
	build((2*node)+1,mid+1,en);
	seg[node].len = seg[2*node].len + seg[(2*node)+1].len;
	seg[node].left = seg[(2*node)+1].left + seg[2*node].left;
	seg[node].right = seg[(2*node)].right + seg[(2*node)+1].right;
	seg[node].answer = seg[(2*node)].left * seg[(2*node)+1].right + (seg[2*node].answer+seg[2*node+1].answer);
	if(st==1 && en == s.length())
		ans = seg[node].answer;
}
int main(){
	int t;
	cin>>t;
	while(t--){
		for(ll i=0;i<500005;i++) seg[i].answer=seg[i].left=seg[i].right=seg[i].len=0;
		cin>>s;
		ans=0;
		build(1,1,s.length());
		cout<<ans<<endl;
	}
}